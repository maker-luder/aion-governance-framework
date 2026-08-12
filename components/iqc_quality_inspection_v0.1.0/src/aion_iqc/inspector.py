from __future__ import annotations
import json,re,subprocess
from dataclasses import dataclass
from datetime import datetime,timezone
from enum import StrEnum
from pathlib import Path
from typing import Any

class CheckStatus(StrEnum): PASS='PASS'; HOLD='HOLD'; FAIL='FAIL'
@dataclass(frozen=True,slots=True)
class InspectionPolicy:
    required_test_target_count:int|None=None; require_public_scan_pass:bool=True; require_canonical_effect_none:bool=True; require_deployment_false:bool=True; require_independent_ivv_unachieved:bool=True; require_external_crosswalk:bool=True; require_ncr_capa_register:bool=True; require_current_coverage_evidence:bool=True; require_traceability:bool=False; require_component_contracts:bool=False; require_qa_reconciliation:bool=False; require_source_state_binding:bool=False
@dataclass(frozen=True,slots=True)
class CheckResult:
    check_id:str; area:str; status:CheckStatus; detail:str; evidence_refs:tuple[str,...]; critical:bool=True
    def as_dict(self): return {'check_id':self.check_id,'area':self.area,'status':self.status.value,'detail':self.detail,'evidence_refs':list(self.evidence_refs),'critical':self.critical}
@dataclass(frozen=True,slots=True)
class IQCReport:
    inspection_id:str; target_head:str; generated_at:str; evaluator_role:str; verdict:CheckStatus; checks:tuple[CheckResult,...]; canonical_effect:str='NONE'; independent_ivv_status:str='NOT_ACHIEVED'; mutation_performed:bool=False
    def as_dict(self): return {'schema_version':'0.1.0','inspection_id':self.inspection_id,'target_head':self.target_head,'generated_at':self.generated_at,'evaluator_role':self.evaluator_role,'verdict':self.verdict.value,'checks':[c.as_dict() for c in self.checks],'canonical_effect':self.canonical_effect,'independent_ivv_status':self.independent_ivv_status,'mutation_performed':self.mutation_performed}
QA={'qa/CURRENT_TEST_RESULTS.json','qa/CURRENT_RELEASE_STATUS_LOCK.json','qa/TEST_RESULTS.md','qa/CURRENT_QA_RECONCILIATION.json','qa/CURRENT_COVERAGE_RESULTS.json','qa/CURRENT_COVERAGE_EVIDENCE.json','qa/COVERAGE_REPORT.md','qa/CURRENT_EVIDENCE_TRACEABILITY.json','qa/IQC_REPORT.json','qa/WHOLE_SYSTEM_VALIDATION.json','qa/INTEGRATION_CANDIDATE_TEST_RESULTS.json','qa/AUTHORITATIVE_REMAINING_GAP_INVENTORY.json','qa/FINAL_LOCAL_GATE_RESULTS.json'}
QA_PREFIXES=('qa/coverage/','qa/current_manifest/','qa/final_current_manifest/')
DOC_GENERATED_PREFIXES=('docs/INTEGRATION_INVENTORY_CURRENT.md','docs/AUTHORITATIVE_REMAINING_GAP_INVENTORY.md')
def J(p):
    try:return json.loads(p.read_text(encoding='utf-8'))
    except FileNotFoundError:return None
def target_records(x):
    if isinstance(x,dict): return x.get('targets')
    return x

def summary(x):
    records=target_records(x)
    if not isinstance(records,list): return 0,0,[],set()
    n=0; f=[]; ts=set()
    for i in records:
        if not isinstance(i,dict):continue
        t=str(i.get('target','')); ts.add(t) if t else None
        m=re.search(r'(?m)^\s*(\d+)\s+passed\b',str(i.get('output',''))); n+=int(m.group(1)) if m else 0
        tested=bool(i.get('tested',True)); returncode=i.get('returncode')
        if returncode is None and not tested: returncode=0
        if returncode!=0:f.append(t or 'UNKNOWN')
    return len(records),n,f,ts
def lc(lock):
    try:return int(str(lock.get('current_tests','')).split()[0])
    except:return None
def R(i,a,s,d,*refs):return CheckResult(i,a,s,d,tuple(refs))
def tests(root,p):
    rs,lk=J(root/'qa/CURRENT_TEST_RESULTS.json'),J(root/'qa/CURRENT_RELEASE_STATUS_LOCK.json'); refs=('qa/CURRENT_TEST_RESULTS.json','qa/CURRENT_RELEASE_STATUS_LOCK.json')
    if not isinstance(target_records(rs),list) or not isinstance(lk,dict):return R('IQC-TEST-001','TEST_EVIDENCE',CheckStatus.HOLD,'inputs missing/invalid',*refs)
    t,n,f,_=summary(rs)
    if f:return R('IQC-TEST-001','TEST_EVIDENCE',CheckStatus.FAIL,'failed targets: '+', '.join(f),*refs)
    if lc(lk)!=n or (isinstance(lk.get('current_targets'),int) and lk['current_targets']!=t) or (p.required_test_target_count is not None and p.required_test_target_count!=t):return R('IQC-TEST-001','TEST_EVIDENCE',CheckStatus.HOLD,'current counts are stale/inconsistent',*refs)
    return R('IQC-TEST-001','TEST_EVIDENCE',CheckStatus.PASS,f'{n} passed across {t} targets',*refs)
def coverage(root,head):
    c,e,t=J(root/'qa/CURRENT_COVERAGE_RESULTS.json'),J(root/'qa/CURRENT_COVERAGE_EVIDENCE.json'),J(root/'qa/CURRENT_TEST_RESULTS.json'); refs=('qa/CURRENT_COVERAGE_RESULTS.json','qa/CURRENT_COVERAGE_EVIDENCE.json','qa/CURRENT_TEST_RESULTS.json')
    if not isinstance(c,list) or not isinstance(e,dict):return R('IQC-MEAS-001','MEASUREMENT',CheckStatus.HOLD,'coverage missing/invalid',*refs)
    records=target_records(t) or []
    ts={str(i.get('target','')) for i in records if isinstance(i,dict) and bool(i.get('tested',True)) and i.get('target')}
    cs={str(i.get('target',i.get('relative_target',''))) for i in c if isinstance(i,dict)}-{''}
    if (ts and ts!=cs) or (head!='UNSPECIFIED' and e.get('target_head')!=head) or e.get('target_count') not in (None,len(c)):return R('IQC-MEAS-001','MEASUREMENT',CheckStatus.HOLD,'coverage evidence is stale/inconsistent',*refs)
    if any(i.get('returncode')!=0 for i in c if isinstance(i,dict)):return R('IQC-MEAS-001','MEASUREMENT',CheckStatus.FAIL,'coverage target failed',*refs)
    return R('IQC-MEAS-001','MEASUREMENT',CheckStatus.PASS,f'coverage covers {len(c)} targets',*refs)
def trace(root,head):
    p=J(root/'qa/CURRENT_EVIDENCE_TRACEABILITY.json'); ref='qa/CURRENT_EVIDENCE_TRACEABILITY.json'; d=p.get('diagnostics',{}) if isinstance(p,dict) else {}
    ok=isinstance(p,dict) and p.get('status')=='PASS' and p.get('criterion_count',0)>0 and p.get('acceptance_decision')=='NOT_EVALUATED' and p.get('canonical_effect')=='NONE' and p.get('deployment') is False and p.get('independent_ivv')=='NOT_ACHIEVED' and p.get('mutation_performed') is False and not d.get('malformed_criteria') and not d.get('missing_local_refs') and (head=='UNSPECIFIED' or p.get('target_head')==head)
    return R('IQC-TRACE-001','TRACEABILITY',CheckStatus.PASS if ok else CheckStatus.HOLD,'traceability structure consistent' if ok else 'traceability missing/stale/incomplete',ref)
def recon(root,head):
    r,t,l=J(root/'qa/CURRENT_QA_RECONCILIATION.json'),J(root/'qa/CURRENT_TEST_RESULTS.json'),J(root/'qa/CURRENT_RELEASE_STATUS_LOCK.json'); refs=('qa/CURRENT_QA_RECONCILIATION.json','qa/CURRENT_TEST_RESULTS.json','qa/CURRENT_RELEASE_STATUS_LOCK.json')
    if not isinstance(r,dict) or not isinstance(target_records(t),list) or not isinstance(l,dict):return R('IQC-RECON-001','QA_RECONCILIATION',CheckStatus.HOLD,'inputs missing/invalid',*refs)
    k,n,f,_=summary(t); ok=r.get('status')=='PASS' and r.get('target_count')==k and r.get('test_count')==n and r.get('failed_targets')==[] and not f and lc(l)==n and l.get('current_targets')==k and r.get('canonical_effect')=='NONE' and r.get('deployment') is False and r.get('independent_ivv')=='NOT_ACHIEVED' and (head=='UNSPECIFIED' or r.get('target_head')==head)
    return R('IQC-RECON-001','QA_RECONCILIATION',CheckStatus.PASS if ok else CheckStatus.HOLD,'reconciliation consistent' if ok else 'reconciliation stale/inconsistent',*refs)
def gov(root,p):
    l=J(root/'qa/CURRENT_RELEASE_STATUS_LOCK.json'); ref='qa/CURRENT_RELEASE_STATUS_LOCK.json'
    if not isinstance(l,dict):return R('IQC-GOV-001','BOUNDARY',CheckStatus.HOLD,'status lock missing/invalid',ref)
    bad=(p.require_canonical_effect_none and l.get('canonical_effect')!='NONE') or (p.require_deployment_false and l.get('deployment') is not False) or (p.require_independent_ivv_unachieved and l.get('independent_ivv')!='NOT_ACHIEVED')
    return R('IQC-GOV-001','BOUNDARY',CheckStatus.FAIL if bad else CheckStatus.PASS,'boundary open' if bad else 'canonical/depoyment/IV&V boundaries closed',ref)
def doc(root,i,a,rel,marks):
    p=root/rel
    if not p.is_file():return R(i,a,CheckStatus.HOLD,'required document missing',rel)
    x=p.read_text(encoding='utf-8'); m=[v for v in marks if v not in x]
    return R(i,a,CheckStatus.HOLD if m else CheckStatus.PASS,'missing markers: '+', '.join(m) if m else 'required markers present', rel)
def pkg(root):
    rs=J(root/'qa/CURRENT_TEST_RESULTS.json'); miss=[]
    records=target_records(rs)
    if not isinstance(records,list):return R('IQC-PKG-001','COMPONENT_CONTRACT',CheckStatus.HOLD,'test results missing','qa/CURRENT_TEST_RESULTS.json')
    for i in records:
        if not isinstance(i,dict) or not bool(i.get('tested',True)):continue
        t=str(i.get('target',''))
        for n in ('README.md','pyproject.toml'):
            if t and not (root/t/n).is_file():miss.append(f'{t}/{n}')
    return R('IQC-PKG-001','COMPONENT_CONTRACT',CheckStatus.HOLD if miss else CheckStatus.PASS,'missing: '+', '.join(miss) if miss else 'package contracts present','qa/CURRENT_TEST_RESULTS.json')
def git(root,*a):return subprocess.check_output(['git',*a],cwd=root,text=True,stderr=subprocess.STDOUT).strip()
def paths(root,*a):return {x for x in git(root,*a).splitlines() if x}
def source(root,head):
    refs=('git:HEAD','git:HEAD^{tree}','git:working-tree')
    try: actual=git(root,'rev-parse','HEAD'); staged=paths(root,'diff','--cached','--name-only'); dirty=paths(root,'diff','--name-only','HEAD')|paths(root,'ls-files','--others','--exclude-standard')
    except (OSError,subprocess.CalledProcessError) as e:return R('IQC-SRC-001','SOURCE_STATE_BINDING',CheckStatus.HOLD,f'git state unavailable: {e}',*refs)
    why=[]
    if head=='UNSPECIFIED':why.append('target head unspecified')
    elif actual!=head:why.append('head mismatch')
    if staged:why.append('staged changes present')
    q=sorted(x for x in dirty if x not in QA and not any(x.startswith(prefix) for prefix in QA_PREFIXES) and x not in DOC_GENERATED_PREFIXES)
    if q:why.append('non-QA drift: '+', '.join(q))
    return R('IQC-SRC-001','SOURCE_STATE_BINDING',CheckStatus.HOLD if why else CheckStatus.PASS,'; '.join(why) if why else 'exact Git source state bound',*refs)
def inspect_repository(root:Path,*,inspection_id='IQC-AION-001',target_head='UNSPECIFIED',policy:InspectionPolicy|None=None,generated_at:str|None=None)->IQCReport:
    p=policy or InspectionPolicy(); c=[]
    if p.require_source_state_binding:c.append(source(root,target_head))
    c.append(tests(root,p))
    if p.require_current_coverage_evidence:c.append(coverage(root,target_head))
    if p.require_traceability:c.append(trace(root,target_head))
    if p.require_component_contracts:c.append(pkg(root))
    if p.require_qa_reconciliation:c.append(recon(root,target_head))
    c.append(gov(root,p))
    if p.require_public_scan_pass:
        l=J(root/'qa/CURRENT_RELEASE_STATUS_LOCK.json'); ok=isinstance(l,dict) and l.get('public_scan')=='PASS'; c.append(R('IQC-REL-001','PUBLIC_RELEASE',CheckStatus.PASS if ok else CheckStatus.HOLD,'public_scan PASS' if ok else 'public_scan not PASS','qa/CURRENT_RELEASE_STATUS_LOCK.json'))
    if p.require_external_crosswalk:c.append(doc(root,'IQC-EVAL-001','EXTERNAL_RULER','docs/C0_EXTERNAL_STANDARDS_CROSSWALK_2026-08-08.md',('ISO/IEC 25040','ISO/IEC 25041','NASA SWE-034','CERTIFICATION_CLAIM = FALSE')))
    if p.require_ncr_capa_register:c.append(doc(root,'IQC-CAPA-001','NCR_CAPA','qa/NCR_CAPA_REGISTER.md',('NCR','Corrective action')))
    v=CheckStatus.FAIL if any(x.status is CheckStatus.FAIL for x in c) else CheckStatus.HOLD if any(x.status is CheckStatus.HOLD for x in c) else CheckStatus.PASS
    return IQCReport(inspection_id,target_head,generated_at or datetime.now(timezone.utc).isoformat(),'REPOSITORY_IQC_INSPECTION_ONLY',v,tuple(c))
