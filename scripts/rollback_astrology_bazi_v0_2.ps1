[CmdletBinding()]
param(
    [switch]$Apply
)

$ErrorActionPreference = 'Stop'
$CoreCommit = 'fe309c5dea63d6d3e60c7103dd5f26abcfe54ab2'
$BaseCommit = '5eae99d67f7d5cc763c4e3361e072d8b7a18688c'
$ExpectedPatchSha256 = '364bc6f40abab7d1a7708709a09f11814b4ccf90c8637892d3de6ed270fa5bb9'
$RepositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PatchFile = Join-Path $RepositoryRoot 'qa\astrology-bazi-v0.2\ASTROLOGY_BAZI_V0_2.patch'

if ((git -C $RepositoryRoot cat-file -t $CoreCommit) -ne 'commit') {
    throw "Core commit is not available: $CoreCommit"
}
git -C $RepositoryRoot merge-base --is-ancestor $CoreCommit HEAD
if ($LASTEXITCODE -ne 0) {
    throw "Core commit is not an ancestor of HEAD: $CoreCommit"
}
$ActualPatchSha256 = (Get-FileHash -LiteralPath $PatchFile -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ActualPatchSha256 -ne $ExpectedPatchSha256) {
    throw "Patch archive SHA-256 mismatch: $ActualPatchSha256"
}

try {
    git -C $RepositoryRoot apply --reverse --check $PatchFile
    if ($LASTEXITCODE -ne 0) { throw 'Reverse-patch verification failed.' }
    Write-Host "ROLLBACK_VERIFY=PASS base=$BaseCommit core=$CoreCommit"

    if (-not $Apply) {
        Write-Host 'ROLLBACK_MODE=DRY_RUN; no repository state changed. Re-run with -Apply on this feature branch.'
        exit 0
    }

    $Branch = git -C $RepositoryRoot branch --show-current
    if ([string]::IsNullOrWhiteSpace($Branch) -or $Branch -eq 'main') {
        throw 'Apply requires a named non-main feature branch.'
    }
    if (-not [string]::IsNullOrWhiteSpace((git -C $RepositoryRoot status --porcelain))) {
        throw 'Apply requires a clean worktree.'
    }
    git -C $RepositoryRoot revert --no-edit $CoreCommit
    if ($LASTEXITCODE -ne 0) { throw 'git revert failed.' }
    Write-Host "ROLLBACK_APPLY=PASS reverted=$CoreCommit branch=$Branch"
} finally { }
