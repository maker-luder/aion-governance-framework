[CmdletBinding()]
param(
    [switch]$Apply
)

$ErrorActionPreference = 'Stop'
$BaseCommit = '79b91226cf3196388432db09760ab0a91c82446d'
$CoreCommit = '0e161368e9596a181d59813630c9fcc87180ab27'
$ExpectedPatchSha256 = '7f763ebae15d2e2618dfb697d77928d73060402b1fb5bf7ca5cd962c6ae26811'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Patch = Join-Path $Root 'qa\astrology-bazi-v0.3\ASTROLOGY_BAZI_V0_3.patch'

if (-not (Test-Path -LiteralPath (Join-Path $Root '.git'))) {
    # A linked worktree stores .git as a file; Test-Path handles both files and directories.
    if (-not (Test-Path -LiteralPath (Join-Path $Root '.git') -PathType Leaf)) {
        throw "Repository metadata not found at $Root"
    }
}

$actualPatchSha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $Patch).Hash.ToLowerInvariant()
if ($actualPatchSha256 -ne $ExpectedPatchSha256) {
    throw "Patch SHA-256 mismatch: expected=$ExpectedPatchSha256 actual=$actualPatchSha256"
}

git -C $Root cat-file -e "$BaseCommit^{commit}"
if ($LASTEXITCODE -ne 0) { throw "Base commit is unavailable: $BaseCommit" }
git -C $Root cat-file -e "$CoreCommit^{commit}"
if ($LASTEXITCODE -ne 0) { throw "Core commit is unavailable: $CoreCommit" }
git -C $Root merge-base --is-ancestor $CoreCommit HEAD
if ($LASTEXITCODE -ne 0) { throw "Core commit is not an ancestor of HEAD: $CoreCommit" }
git -C $Root apply --unidiff-zero --cached --reverse --check $Patch
if ($LASTEXITCODE -ne 0) { throw 'Patch reverse-check against the Git index failed' }

Write-Output "ROLLBACK_VERIFY=PASS base=$BaseCommit core=$CoreCommit patch_sha256=$actualPatchSha256"

if (-not $Apply) {
    Write-Output 'ROLLBACK_MODE=DRY_RUN'
    Write-Output "ROLLBACK_COMMAND=powershell -ExecutionPolicy Bypass -File `"$PSCommandPath`" -Apply"
    exit 0
}

if (@(git -C $Root status --porcelain).Count -ne 0) {
    throw 'Apply mode requires a clean worktree'
}

git -C $Root revert --no-edit $CoreCommit
if ($LASTEXITCODE -ne 0) { throw "git revert failed for $CoreCommit" }

$newHead = (git -C $Root rev-parse HEAD).Trim()
Write-Output 'ROLLBACK_MODE=APPLY'
Write-Output "ROLLBACK_REVERT_COMMIT=$newHead"
Write-Output "ROLLBACK_REVERTED_CORE=$CoreCommit"
