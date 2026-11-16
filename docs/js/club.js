(()=>{
const SBU='https://xkbgsoppludqxdgfjlcd.supabase.co',KEY='sb_publishable_RDj-YzmEX4dK_T_0e4Qwrg_otjui5g5',DOM='@ftc-club.test',B='shots';
const sb=window.supabase.createClient(SBU,KEY);
const ST={new:'waiting',ok:'accepted',redo:'redo'};
const h=(t,a={},...c)=>{const e=document.createElement(t);for(const k in a){if(k.startsWith('on'))e.addEventListener(k.slice(2),a[k]);else if(k==='html')e.innerHTML=a[k];else e.setAttribute(k,a[k])}for(const x of c.flat())if(x!=null)e.append(x.nodeType?x:document.createTextNode(x));return e};
const dt=s=>new Date(s).toLocaleString([], {day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'});
let me=null;
async function who(){const {data:{session}}=await sb.auth.getSession();if(!session)return null;const {data}=await sb.from('profiles').select('id,name,is_admin').eq('id',session.user.id).single();return data}
function login(box,done){
  const u=h('input',{placeholder:'name',autocomplete:'username'}),p=h('input',{type:'password',placeholder:'password',autocomplete:'current-password'}),m=h('span',{class:'cl-err'});
  const go=async e=>{e.preventDefault();m.textContent='';const {error}=await sb.auth.signInWithPassword({email:u.value.trim().toLowerCase()+DOM,password:p.value});if(error){m.textContent='Wrong name or password';return}location.reload()};
  box.replaceChildren(h('form',{class:'cl-login',onsubmit:go},u,p,h('button',{type:'submit'},'Sign in'),m));
}
async function urls(paths){if(!paths.length)return{};const {data}=await sb.storage.from(B).createSignedUrls(paths,3600);const r={};(data||[]).forEach(x=>r[x.path]=x.signedUrl);return r}
function thread(s,cs,onsend){
  const t=h('textarea',{rows:2,placeholder:'Comment…'});
  const send=async()=>{const b=t.value.trim();if(!b)return;const {error}=await sb.from('comments').insert({submission_id:s.id,body:b});if(error){alert(error.message);return}onsend()};
  return h('div',{class:'cl-thread'},cs.map(c=>h('div',{class:'cl-c'+(c.profiles?.name===me.name?' cl-mine':'')},h('b',{},c.profiles?.name||'?'),' ',h('small',{},dt(c.created_at)),h('div',{},c.body))),h('div',{class:'cl-reply'},t,h('button',{onclick:send},'Send')));
}
function card(s,u,cs,reload,admin){
  const img=h('a',{href:u[s.path]||'#',target:'_blank'},h('img',{src:u[s.path]||'',loading:'lazy'}));
  const set=async v=>{const {data,error}=await sb.from('submissions').update({status:v}).eq('id',s.id).select('id');if(error)alert(error.message);else if(!data.length)alert('Not saved: no permission');else reload()};
  const del=async()=>{if(!confirm('Delete this submission?'))return;await sb.storage.from(B).remove([s.path]);await sb.from('submissions').delete().eq('id',s.id);reload()};
  return h('div',{class:'cl-card'},img,h('div',{class:'cl-body'},
    h('div',{},admin?h('b',{},(s.profiles?.name||'?')+' · '+s.task.toUpperCase()+' '):null,h('span',{class:'cl-st cl-'+s.status},ST[s.status]),' ',h('small',{},dt(s.created_at)),
      admin?[' ',h('button',{onclick:()=>set('ok')},'✔ Accept'),h('button',{onclick:()=>set('redo')},'↻ Redo')]:null,
      (admin||s.status==='new')?h('button',{class:'cl-del',onclick:del},'Delete'):null),
    s.note?h('div',{class:'cl-note'},s.note):null,
    thread(s,cs,reload)));
}
async function load(q){
  const {data:ss,error}=await q.order('created_at',{ascending:false});if(error)return{ss:[],u:{},cm:{}};
  const u=await urls(ss.map(s=>s.path));const cm={};
  if(ss.length){const {data:cs}=await sb.from('comments').select('*,profiles(name)').in('submission_id',ss.map(s=>s.id)).order('created_at');(cs||[]).forEach(c=>(cm[c.submission_id]=cm[c.submission_id]||[]).push(c))}
  return{ss,u,cm};
}
async function widget(box){
  const task=box.dataset.task;
  if(!me){login(box);return}
  const list=h('div'),f=h('input',{type:'file',accept:'image/*'}),n=h('input',{placeholder:'Note (optional)'}),m=h('span',{class:'cl-err'});
  let file=null;f.onchange=()=>{file=f.files[0]};
  const up=async()=>{if(!file){m.textContent='Choose or paste a screenshot first';return}m.textContent='Uploading…';
    const ext=(file.type.split('/')[1]||'png').replace('jpeg','jpg'),path=`${me.id}/${task}/${Date.now()}.${ext}`;
    let {error}=await sb.storage.from(B).upload(path,file,{contentType:file.type});if(error){m.textContent=error.message;return}
    ({error}=await sb.from('submissions').insert({task,path,note:n.value.trim()||null}));if(error){m.textContent=error.message;return}
    m.textContent='';n.value='';f.value='';file=null;draw()};
  box.addEventListener('paste',e=>{const it=[...e.clipboardData.items].find(i=>i.type.startsWith('image/'));if(it){file=it.getAsFile();m.textContent='Screenshot pasted ✔'}});
  const draw=async()=>{const {ss,u,cm}=await load(sb.from('submissions').select('*').eq('task',task).eq('user_id',me.id));list.replaceChildren(...ss.map(s=>card(s,u,cm[s.id]||[],draw,false)))};
  box.replaceChildren(h('div',{class:'cl-head'},h('b',{},'Your submission'),h('small',{},' signed in as '+me.name+' · ',h('a',{href:'#',onclick:async e=>{e.preventDefault();await sb.auth.signOut();location.reload()}},'sign out'))),
    h('div',{class:'cl-up',tabindex:0},f,n,h('button',{onclick:up},'Submit'),m,h('div',{class:'cl-hint'},'Pick a file or click here and press Ctrl/Cmd+V to paste a screenshot.')),list);
  draw();
}
async function review(box){
  if(!me){login(box);return}
  const adm=me.is_admin;
  const {data:ps}=await sb.from('profiles').select('id,name').eq('is_admin',false).order('name');
  const tasks=box.dataset.tasks.split(',');
  const req=new Set((box.dataset.req||'').split(','));
  const fs=h('select',{},h('option',{value:''},'all statuses'),Object.entries(ST).map(([k,v])=>h('option',{value:k},v)));
  const ft=h('select',{},h('option',{value:''},'all tasks'),tasks.map(t=>h('option',{value:t},t.toUpperCase())));
  const fp=h('select',{},h('option',{value:''},'all students'),(ps||[]).map(p=>h('option',{value:p.id},p.name)));
  fs.value='new';
  const grid=h('div',{class:'cl-grid'}),list=h('div');
  const draw=async()=>{
    const {data:all,error}=await sb.rpc('overview');if(error){grid.textContent='Table error: '+error.message}
    const last={},cnt={};(all||[]).forEach(s=>{const k=s.user_id+s.task;last[k]=s.status;cnt[k]=(cnt[k]||0)+1});
    const SY={ok:'+',redo:'−',new:'?'};
    const pick=(p,t)=>{fp.value=p;ft.value=t;fs.value='';draw()};
    const sum=p=>tasks.filter(t=>last[p.id+t]==='ok').length;
    const rows=[...(ps||[])].sort((a,b)=>sum(b)-sum(a)||a.name.localeCompare(b.name));
    if(!error)grid.replaceChildren(h('table',{class:'cl-t'},h('tr',{},h('th'),h('th',{title:'accepted'},'Σ'),tasks.map(t=>h('th',{class:req.has(t)?'cl-rq':'',title:req.has(t)?'required':''},t[0]==='l'?t[1]+'.'+t.slice(2):t.slice(1)))),rows.map(p=>h('tr',{class:p.id===me.id?'cl-me':''},h('td',{class:'cl-n'},p.name),h('td',{class:'cl-sum'},String(sum(p))),tasks.map(t=>{const k=p.id+t,v=last[k];const a={class:v?'cl-'+v:'',title:v?ST[v]+' · '+cnt[k]+' submission(s)':''};if(v&&adm)a.onclick=()=>pick(p.id,t);return h('td',a,v?SY[v]:'')})))),
      h('small',{},'+ accepted · − redo · ? waiting · orange number = required. The latest submission counts.'+(adm?' Click a cell to see it.':'')));
    if(!adm)return;
    let q=sb.from('submissions').select('*,profiles(name)');if(fs.value)q=q.eq('status',fs.value);if(ft.value)q=q.eq('task',ft.value);if(fp.value)q=q.eq('user_id',fp.value);
    const {ss,u,cm}=await load(q);list.replaceChildren(ss.length?'':'Nothing here.',...ss.map(s=>card(s,u,cm[s.id]||[],draw,true)));
  };
  [fs,ft,fp].forEach(e=>e.onchange=draw);
  box.replaceChildren(grid,...(adm?[h('h2',{},'Submissions'),h('div',{class:'cl-filters'},fs,ft,fp),list]:[]));
  draw();
}
function base(){const l=document.querySelector('a.md-logo,a.md-header__button[href]');return new URL(l?l.getAttribute('href'):'./',location)}
function account(){
  const hdr=document.querySelector('.md-header__inner');if(!hdr)return;
  const box=h('div',{class:'cl-acct'}),tbl=new URL('review/',base()).href;
  if(me){
    box.append(h('a',{href:tbl},'Table'),h('span',{class:'cl-who'},me.name),h('a',{href:'#',onclick:async e=>{e.preventDefault();await sb.auth.signOut();location.reload()}},'Sign out'));
  }else{
    const pop=h('div',{class:'cl-pop',hidden:''});login(pop);
    box.append(h('a',{href:'#',onclick:e=>{e.preventDefault();pop.hidden=!pop.hidden;const i=pop.querySelector('input');if(i&&!pop.hidden)i.focus()}},'Sign in'),pop);
  }
  const s=hdr.querySelector('.md-search');hdr.insertBefore(box,s||null);
}
(async()=>{
  const ws=document.querySelectorAll('.cl-sub[data-task]'),rv=document.getElementById('cl-review');
  try{me=await who()}catch(e){console.error(e)}
  try{account()}catch(e){console.error(e)}
  ws.forEach(widget);if(rv)review(rv);
})();
})();
