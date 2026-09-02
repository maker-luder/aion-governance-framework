[CmdletBinding()]
param(
    [switch]$Apply
)

$ErrorActionPreference = 'Stop'
$BaseCommit = 'bb3e5e092c11a1b582a163422611308aaeab1f01'
$CoreCommit = '0199d3edb506cc0b85afca45880ba43df3481a43'
$ExpectedPatchSha256 = '8a08a3e8e9dce8497821605d6c0530b315d91c8df1edf1bc02a4cc8fc358dfd9'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Patch = Join-Path $Root 'qa\zi-wei-dou-shu-v0.1\ZI_WEI_DOU_SHU_V0_1.patch'

if (-not (Test-Path -LiteralPath (Join-Path $Root '.git'))) {
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
