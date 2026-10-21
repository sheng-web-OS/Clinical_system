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
