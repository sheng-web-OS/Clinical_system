(()=>{const $=s=>document.querySelector(s);const root=document.body;try{const t=localStorage.getItem("clinical-theme");if(t==="dark")root.classList.add("dark");const z=localStorage.getItem("clinical-font");if(z)document.documentElement.style.setProperty("--text-size",z+"px")}catch(e){}const bind=(id,cb)=>{$("#"+id)?.addEventListener("click",cb)};bind("theme",()=>{root.classList.toggle("dark");try{localStorage.setItem("clinical-theme",root.classList.contains("dark")?"dark":"light")}catch(e){}});for(const [id,delta] of [["fontplus",1],["fontminus",-1]])bind(id,()=>{let val=parseInt(getComputedStyle(document.documentElement).getPropertyValue("--text-size"),10)||18;val=Math.min(24,Math.max(15,val+delta));document.documentElement.style.setProperty("--text-size",val+"px");try{localStorage.setItem("clinical-font",String(val))}catch(e){}});bind("mobilemenu",()=>$(".sidebar")?.classList.toggle("open"));const bar=$(".floating");addEventListener("scroll",()=>{if(!bar)return;const h=document.documentElement.scrollHeight-innerHeight;bar.style.width=(h>0?(scrollY/h)*100:100)+"%"},{passive:true});const input=$("#search");if(input){Promise.resolve(window.CLINICAL_INDEX||[]).then(rows=>{input.addEventListener("input",()=>{const q=input.value.trim().toLowerCase();const out=$("#results");if(!out)return;out.replaceChildren();if(q.length<2)return;let count=0;for(const row of rows){const idx=row.text.toLowerCase().indexOf(q);if(idx<0)continue;const a=document.createElement("a");a.className="result";a.href=row.url;const b=document.createElement("b");b.textContent=row.title;const t=document.createElement("small");t.textContent=row.text.slice(Math.max(idx-45,0),idx+90);a.append(b,t);out.append(a);if(++count>=8)break}if(!count)out.textContent="沒有符合結果"})}).catch(()=>{})} })();
// Teaching model: preserve the complete explanation without requiring JavaScript.
(()=>{
 const model=document.querySelector('[data-oxygen-model]');
 if(model){
  const hb=model.querySelector('#hb-slider'),co=model.querySelector('#co-slider');
  const write=(id,value)=>{model.querySelector('#'+id).textContent=value};
  const update=()=>{
   const h=Number(hb.value),c=Number(co.value),content=1.34*h*.98+.003*100,delivery=content*c*10;
   write('hb-value',h.toFixed(1).replace(/\.0$/,''));write('co-value',c.toFixed(1));
   write('cao2-value',content.toFixed(1));write('do2-value',Math.round(delivery).toLocaleString('en-US'));
   const reason=h<15&&c<5?'血紅素與心輸出同時下降，含量和血流的影響相乘。':h<15?'血紅素減少，每單位血能帶的氧就減少。':c<5?'血流減少，即使血液氧合良好，每分鐘送達的總氧仍下降。':'改變血紅素或血流，即可看見含量與輸送量的不同。';
   write('oxygen-explanation',reason+' 飽和度固定 98%；此處總氧輸送約 '+Math.round(delivery).toLocaleString('en-US')+' mL/min。');
  };
  hb.addEventListener('input',update);co.addEventListener('input',update);update();
 }
 const links=[...document.querySelectorAll('.reader-outline a')];
 if(links.length&&'IntersectionObserver' in window){
  const ob=new IntersectionObserver(entries=>{for(const e of entries)if(e.isIntersecting){for(const a of links){const current=a.getAttribute('href')==='#'+e.target.id;a.classList.toggle('current',current);if(current)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current')}}},{rootMargin:'-8% 0px -65% 0px'});
  for(const link of links){const heading=document.getElementById(link.getAttribute('href').slice(1));if(heading)ob.observe(heading)}
 }
})();

/* Library affordances are optional; the complete article and links work without JS. */
(()=>{
  const page=document.body;
  if(page.classList.contains('lesson-page')){
    const title=document.querySelector('.reader-hero h1')?.textContent?.trim();
    const path=window.location.pathname.split('/').pop();
    if(title && path && /^[a-z0-9-]+\.html$/.test(path)){
      try{localStorage.setItem('clinical-last-read',JSON.stringify({title,url:path}))}catch(e){}
    }
  }
  if(!page.classList.contains('library-page'))return;
  const buttons=[...document.querySelectorAll('[data-library-filter]')];
  const cards=[...document.querySelectorAll('.library-card')];
  const grid=document.querySelector('#library-grid');
  const empty=document.querySelector('#library-filter-empty');
  for(const button of buttons){
    button.addEventListener('click',()=>{
      const filter=button.dataset.libraryFilter;
      for(const target of buttons){
        const active=target===button;
        target.classList.toggle('is-active',active);
        target.setAttribute('aria-pressed',String(active));
      }
      let visible=0;
      for(const card of cards){
        const show=filter==='all'||card.dataset.collection===filter;
        card.hidden=!show;
        if(show)visible++;
      }
      grid?.classList.toggle('is-filtered',filter!=='all');
      if(empty)empty.hidden=visible>0;
    });
  }
  const input=document.querySelector('#search');
  document.addEventListener('keydown',e=>{
    const t=e.target;
    if(e.key==='/' && !e.altKey && !e.metaKey && !e.ctrlKey &&
       !['INPUT','TEXTAREA','SELECT'].includes(t?.tagName) && !t?.isContentEditable){
      e.preventDefault();input?.focus();
    }else if(e.key==='Escape' && document.activeElement===input){
      input.value='';input.dispatchEvent(new Event('input'));input.blur();
    }
  });
  try{
    const read=JSON.parse(localStorage.getItem('clinical-last-read')||'null');
    if(read&&typeof read.title==='string'&&typeof read.url==='string'&&
       /^[a-z0-9-]+\.html$/.test(read.url)&&cards.some(c=>c.getAttribute('href')===read.url)){
      const link=document.querySelector('#resume-reading');
      const title=document.querySelector('#resume-title');
      if(link && title){link.href=read.url;title.textContent=read.title;link.hidden=false}
    }
  }catch(e){}
})();


/* Clinical-case reading: evidence is disclosed only after a reasoned choice.
   No quiz responses or timings are stored or transmitted. */
(()=>{
 const lab=document.querySelector('[data-case-sequence]');
 const stages=lab?[...lab.querySelectorAll('[data-case-stage]')]:[];
 const analysis=document.querySelector('[data-case-analysis]');
 if(!lab||!analysis||stages.length!==4)return;
 const finish=lab.querySelector('[data-case-complete]');
 const progress=lab.querySelector('[data-case-progress]');
 const enabled='case-sequence-enabled',unlocked='case-sequence-complete';
 document.body.classList.add(enabled);
 const showAnalysis=()=>{
   document.body.classList.add(unlocked);
   if(finish)finish.hidden=false;
   analysis.scrollIntoView({behavior:'smooth',block:'start'});
 };
 const reset=()=>{
   document.body.classList.remove(unlocked);
   for(const [i,stage] of stages.entries()){
     stage.hidden=i!==0;
     for(const radio of stage.querySelectorAll('input[type=radio]'))radio.checked=false,radio.disabled=false;
     for(const option of stage.querySelectorAll('.case-option'))option.classList.remove('case-choice-correct','case-choice-wrong');
     const btn=stage.querySelector('[data-case-submit]'),next=stage.querySelector('[data-case-next]'),
           status=stage.querySelector('.case-alert'), rationale=stage.querySelector('[data-case-rationale]');
     if(btn)btn.disabled=false;
     if(next)next.hidden=true;
     if(status){status.hidden=true;status.textContent=''}
     if(rationale)rationale.hidden=true;
   }
   if(finish)finish.hidden=true;
   if(progress)progress.textContent='1 / 4';
   stages[0].scrollIntoView({behavior:'smooth',block:'start'});
 };
 for(const [i,stage] of stages.entries()){
   const submit=stage.querySelector('[data-case-submit]');
   const next=stage.querySelector('[data-case-next]');
   if(!submit||!next)continue;
   submit.addEventListener('click',()=>{
     const chosen=stage.querySelector('input[type=radio]:checked');
     const status=stage.querySelector('.case-alert');
     if(!chosen){
       status.hidden=false;
       status.textContent='請先選一個推論，再檢查下一項證據。';
       return;
     }
     const correct=stage.dataset.caseCorrect;
     for(const option of stage.querySelectorAll('.case-option')){
       const radio=option.querySelector('input');
       radio.disabled=true;
       option.classList.toggle('case-choice-correct',radio.value===correct);
       option.classList.toggle('case-choice-wrong',radio.checked&&radio.value!==correct);
     }
     status.hidden=false;
     status.textContent=chosen.value===correct?'這項判斷符合目前證據。':'這項判斷超出了目前證據；核對下方的因果推導。';
     stage.querySelector('[data-case-rationale]').hidden=false;
     submit.disabled=true;
     next.hidden=false;
     next.focus();
   });
   next.addEventListener('click',()=>{
     stage.hidden=true;
     if(i===stages.length-1){
       showAnalysis();
     }else{
       stages[i+1].hidden=false;
       if(progress)progress.textContent=(i+2)+' / 4';
       stages[i+1].scrollIntoView({behavior:'smooth',block:'start'});
       stages[i+1].querySelector('input[type=radio]')?.focus({preventScroll:true});
     }
   });
 }
 lab.querySelector('[data-case-skip]')?.addEventListener('click',showAnalysis);
 lab.querySelector('[data-case-restart]')?.addEventListener('click',reset);
})();


// Reading quality: convert wide medical comparison tables into mobile cards.
// The original semantic <table> stays unchanged on desktop and for screen readers.
(()=>{
  for(const table of document.querySelectorAll('.reading-prose table')){
    const labels=[...table.querySelectorAll('thead th')].map(el=>el.textContent.trim());
    if(labels.length<3 || labels.some(x=>!x) || table.querySelector('td[colspan], th[colspan], td[rowspan]'))continue;
    const rows=[...table.querySelectorAll('tbody tr')];
    if(!rows.length || rows.some(tr=>tr.querySelectorAll('td').length!==labels.length))continue;
    for(const tr of rows){
      [...tr.querySelectorAll('td')].forEach((cell,index)=>cell.setAttribute('data-label',labels[index]));
    }
    table.classList.add('reading-mobile-cards');
  }
})();
