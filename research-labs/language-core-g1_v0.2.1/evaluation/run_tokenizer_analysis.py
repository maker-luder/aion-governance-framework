from pathlib import Path
import argparse,json,hashlib
def main():
 p=argparse.ArgumentParser();p.add_argument('--model',type=Path,required=True);p.add_argument('--dataset',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 try: from transformers import AutoTokenizer
 except ImportError as e: raise SystemExit(f'pinned tokenizer runtime missing: {e}')
 tok=AutoTokenizer.from_pretrained(str(a.model),local_files_only=True,trust_remote_code=False)
 rows=[json.loads(x) for x in a.dataset.read_text(encoding='utf-8').splitlines() if x.strip()];out=[]
 for r in rows:
  tw=r['zh_tw_prompt'];cn=r['zh_cn_prompt'];tw_n=len(tok.encode(tw,add_special_tokens=False));cn_n=len(tok.encode(cn,add_special_tokens=False));out.append({'pair_id':r['pair_id'],'tw_tokens':tw_n,'cn_tokens':cn_n,'tw_token_per_char':tw_n/max(1,len(tw)),'cn_token_per_char':cn_n/max(1,len(cn))})
 result={'execution_status':'EXECUTED','records':out,'tokenizer_source':str(a.model),'dataset_sha256':hashlib.sha256(a.dataset.read_bytes()).hexdigest()};a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
