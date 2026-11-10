(()=>{'use strict';
const DATA=window.DANTAS_DATA||{recipes:[],techniques:[],workshops:[],videos:[]};
const RECIPES=[...(DATA.recipes||[])].sort((a,b)=>(b.createdAt||'').localeCompare(a.createdAt||''));
const STORAGE_KEY='dantas-cozinha-v1';
const cleanState=()=>({favorites:[],notes:{},planner:{},shoppingChecked:{}});
let state=readState(),selectedFilter='todas',selectedSearch='',selectedSchoolCategory='todas',selectedSchoolSearch='',modalRecipe=null,modalServings=1;
function readState(){try{const x=JSON.parse(localStorage.getItem(STORAGE_KEY)||'null');return x&&typeof x==='object'?{...cleanState(),...x,favorites:Array.isArray(x.favorites)?x.favorites:[],notes:x.notes||{},planner:x.planner||{},shoppingChecked:x.shoppingChecked||{}}:cleanState()}catch{return cleanState()}}
function saveState(){try{localStorage.setItem(STORAGE_KEY,JSON.stringify(state))}catch{toast('Não foi possível salvar neste navegador.')}}
function el(id){return document.getElementById(id)}
function esc(x){return String(x??'').replace(/[&<>"']/g,s=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[s]))}
function safeUrl(x){try{const u=new URL(x);return ['http:','https:'].includes(u.protocol)?u.href:'#'}catch{return '#'}}
function toast(message){const t=el('toast');t.textContent=message;t.classList.add('show');clearTimeout(toast.timeout);toast.timeout=setTimeout(()=>t.classList.remove('show'),2700)}
const categoryName={entrada:'Entrada',principal:'Prato principal',sobremesa:'Sobremesa'};
function img(x){return `<img src="${esc(safeUrl(x.image||''))}" loading="lazy" decoding="async" alt="Imagem ilustrativa associada à receita: ${esc(x.title)}" onerror="this.onerror=null;this.src='assets/recipe-placeholder.svg'">`}
function imageAttribution(r){return `<figcaption class="recipe-image-credit"><strong>Imagem ilustrativa</strong>${r.imageCredit?` · ${esc(r.imageCredit)}`:''}<span> A apresentação pode ser diferente do resultado desta receita.</span></figcaption>`}
function isFav(id){return state.favorites.includes(id)}
function card(r){return `<article class="recipe-card"><div class="recipe-photo" data-recipe="${esc(r.id)}"><div class="photo-fallback">${esc(r.emoji||'🍽️')}</div>${img(r)}<span class="badge">${esc(categoryName[r.category]||'Receita')}</span><button class="heart ${isFav(r.id)?'saved':''}" data-fav="${esc(r.id)}" aria-label="${isFav(r.id)?'Remover dos':'Salvar nos'} favoritos" title="Favoritos">${isFav(r.id)?'♥':'♡'}</button></div><div class="recipe-content"><h3 class="recipe-title" data-recipe="${esc(r.id)}">${esc(r.title)}</h3><p class="recipe-desc">${esc(r.description)}</p><div class="recipe-info"><span>◷ ${esc(r.minutesLabel || (r.minutes + ' min'))}</span><span>✳ ${esc(r.difficulty)}</span><span>♙ ${esc(r.servingsLabel || (r.servings + ' porções'))}</span></div><div class="card-bottom"><button class="inline-link" data-recipe="${esc(r.id)}">Ver receita →</button><button class="mini-add" data-plan-add="${esc(r.id)}" title="Adicionar ao próximo espaço vazio do cardápio">+ cardápio</button></div></div></article>`}
function updateFavCount(){el('fav-count').textContent=state.favorites.length}
function renderRecipes(){const term=selectedSearch.trim().toLocaleLowerCase('pt-BR');const arr=RECIPES.filter(r=>(selectedFilter==='todas'||selectedFilter==='favoritas'&&isFav(r.id)||r.category===selectedFilter)&&(!term||[r.title,r.description,...(r.ingredients||[]).map(i=>typeof i==='string'?i:i.name)].join(' ').toLocaleLowerCase('pt-BR').includes(term)));
el('recipe-list').innerHTML=arr.length?arr.map(card).join(''):'<div class="empty-state"><strong>Nenhuma receita por aqui.</strong> Experimente outro filtro ou termo de busca.</div>';el('recipes-count').textContent=`${arr.length} ${arr.length===1?'receita encontrada':'receitas encontradas'}`;document.querySelectorAll('#recipe-filters .chip').forEach(b=>b.classList.toggle('selected',b.dataset.filter===selectedFilter));updateFavCount()}
function renderCuratedDiscoveries(){
const root=el('curation-list');if(!root)return;
const discoveries=[...(DATA.curatedDiscoveries||[])].sort((a,b)=>(b.createdAt||'').localeCompare(a.createdAt||''));
root.innerHTML=discoveries.length?discoveries.map(item=>`<article class="curation-card">
<div class="curation-card-top"><span class="tech-pill">${esc(categoryName[item.category]||'Receita')}</span><span class="curation-verified">Fonte verificada · ${esc(item.verifiedAt)}</span></div>
<h3>${esc(item.title)}</h3>
<p>${esc(item.description)}</p>
<div class="curation-ingredients"><strong>Ingredientes principais</strong><ul>${(item.mainIngredients||[]).map(i=>`<li>${esc(i)}</li>`).join('')}</ul></div>
<div class="curation-credit"><span>Autoria: <b>${esc(item.author)}</b></span><span>Fonte: ${esc(item.sourceName)}</span></div>
<a class="btn primary" href="${esc(safeUrl(item.sourceUrl))}" target="_blank" rel="noopener noreferrer" aria-label="Ver preparo original de ${esc(item.title)} em ${esc(item.sourceName)}">Ver preparo na fonte original ↗</a>
<small>Ficha editorial, sem reprodução do preparo ou alegação de teste pelo portal.</small>
</article>`).join(''):'<p>Nenhuma seleção editorial nova nesta semana.</p>';
}
function renderHome(){el('home-recipes').innerHTML=RECIPES.slice(0,3).map(card).join('')}
// Escola: blocos didáticos opcionais; conteúdo legado continua acessível.
function schoolBlock(block){
 if(!block||typeof block!=='object')return '';
 const title=block.title?`<h5>${esc(block.title)}</h5>`:'';
 const items=Array.isArray(block.items)?block.items:[];
 const list=(tag,values)=>`<${tag}>${values.map(v=>`<li>${esc(v)}</li>`).join('')}</${tag}>`;
 switch(block.type){
 case 'bullets':if(!items.length)return '';return `<div class="school-block school-list">${title}${list('ul',items)}</div>`;
 case 'steps':if(!items.length)return '';return `<div class="school-block school-steps">${title}${list('ol',items)}</div>`;
 case 'callout':return `<aside class="school-block school-callout" aria-label="${esc(block.title||'Dica')}"><span aria-hidden="true">✦</span><div>${title}<p>${esc(block.text||'')}</p></div></aside>`;
 case 'image':{const url=safeUrl(block.src||'');if(url==='#'||!block.alt)return '';return `<figure class="school-block school-image"><img src="${esc(url)}" alt="${esc(block.alt)}" loading="lazy" decoding="async"><figcaption>${esc(block.caption||'')}${block.credit?` · ${esc(block.credit)}`:''}</figcaption></figure>`;}
 case 'workflow':{if(!items.length)return '';return `<section class="school-block school-flow" aria-label="${esc(block.title||'Fluxo de trabalho')}">${title}<ol>${items.map((v,i)=>`<li><span aria-hidden="true">${i+1}</span><strong>${esc(v)}</strong></li>`).join('')}</ol></section>`;}
 case 'orgchart':{if(!items.length)return '';return `<section class="school-block school-org" aria-label="${esc(block.title||'Hierarquia')}">${title}<ol>${items.map((v,i)=>`<li style="--level:${Math.min(i,4)}"><span aria-hidden="true">↳</span>${esc(v)}</li>`).join('')}</ol></section>`;}
 case 'glossary':if(!items.length)return '';return `<div class="school-block school-glossary">${title}<dl>${items.filter(v=>v&&typeof v==='object').map(v=>`<dt>${esc(v.term)}</dt><dd>${esc(v.definition)}</dd>`).join('')}</dl></div>`;
 default:return '';
 }
}
function schoolParagraphs(value){return String(value||'').split(/\n\s*\n/).filter(Boolean).map(p=>`<p>${esc(p)}</p>`).join('')}
function renderSchoolFilters(){
 const root=el('school-filters');if(!root)return;
 const categories=['todas',...new Set((DATA.techniques||[]).map(t=>t.category).filter(Boolean))];
 root.innerHTML=categories.map(c=>`<button type="button" class="chip ${selectedSchoolCategory===c?'selected':''}" data-school-category="${esc(c)}" aria-pressed="${selectedSchoolCategory===c}">${esc(c==='todas'?'Todas as aulas':c)}</button>`).join('');
}
function renderTechniques(){
 const root=el('tech-grid');if(!root)return;
 const term=selectedSchoolSearch.trim().toLocaleLowerCase('pt-BR');
 const lessons=(DATA.techniques||[]).filter(t=>(selectedSchoolCategory==='todas'||t.category===selectedSchoolCategory)&&(!term||[t.title,t.summary,t.category,...(t.lesson||[]).map(s=>s.heading)].join(' ').toLocaleLowerCase('pt-BR').includes(term)));
 const count=el('school-count');if(count)count.textContent=`${lessons.length} ${lessons.length===1?'aula encontrada':'aulas encontradas'}`;
 root.innerHTML=lessons.length?lessons.map((t,i)=>`<details class="tech-card" id="escola-${esc(t.id)}">
 <summary><div class="tech-summary"><div class="tech-number">${String(i+1).padStart(2,'0')} <span class="tech-pill"> · ${esc(t.category)}</span></div><h3>${esc(t.title)}</h3><p>${esc(t.summary)}</p><span class="school-card-meta">${(t.lesson||[]).length} seções · Exercício prático</span></div><span class="tech-toggle" aria-hidden="true"></span></summary>
 <div class="tech-detail"><div class="school-intro"><span class="school-kicker">CADERNO DE APRENDIZADO</span><p>${esc(t.summary)}</p></div>
 <div class="tech-lesson"><h4>Por que importa</h4>${schoolParagraphs(t.why)}</div>
 <nav class="school-contents" aria-label="Sumário da aula"><strong>Nesta aula</strong><ol>${(t.lesson||[]).map((section,j)=>`<li><a href="#aula-${esc(t.id)}-${j}" data-school-anchor="aula-${esc(t.id)}-${j}">${esc(section.heading)}</a></li>`).join('')}</ol></nav>
 ${(t.lesson||[]).map((section,j)=>`<section class="tech-lesson" id="aula-${esc(t.id)}-${j}"><h4><span class="school-section-number">${String(j+1).padStart(2,'0')}</span> ${esc(section.heading)}</h4>${schoolParagraphs(section.body)}${(section.blocks||[]).map(schoolBlock).join('')}</section>`).join('')}
 ${(t.contentBlocks||[]).map(schoolBlock).join('')}
 ${t.deepDive?`<div class="tech-lesson school-deep-dive"><h4>Para aprofundar</h4>${schoolParagraphs(t.deepDive)}</div>`:''}
 <div class="tech-lesson tech-practice"><h4>✦ Experimente na cozinha</h4>${schoolParagraphs(t.practice)}</div>
 ${t.mistakes?.length?`<div class="tech-lesson school-mistakes"><h4>Erros comuns</h4><ul>${t.mistakes.map(m=>`<li>${esc(m)}</li>`).join('')}</ul></div>`:''}
 </div></details>`).join(''):'<div class="empty-state">Nenhuma aula encontrada. Tente outro termo ou categoria.</div>';
 renderSchoolFilters();
}
function renderWorkshops(){const now=new Date();const today=[now.getFullYear(),String(now.getMonth()+1).padStart(2,'0'),String(now.getDate()).padStart(2,'0')].join('-');el('workshop-list').innerHTML=(DATA.workshops||[]).filter(w=>!w.eventDate||w.eventDate>=today).map((w,i)=>`<article class="workshop-card"><div class="workshop-head"><span class="workshop-letter">${['A','I','G'][i%3]}</span><span class="workshop-tag">${esc(w.tag)}</span></div><h3>${esc(w.name)}</h3><div class="workshop-location">📍 ${esc(w.neighborhood)} · ${esc(w.address)}</div><p>${esc(w.description)}</p><div class="workshop-links"><a href="${esc(safeUrl(w.url))}" target="_blank" rel="noopener noreferrer">${w.eventDate?"Detalhes e inscrição ↗":"Site e programação ↗"}</a>${w.instagram?`<a href="${esc(safeUrl(w.instagram))}" target="_blank" rel="noopener noreferrer">Instagram ↗</a>`:''}</div></article>`).join('')}
function renderVideos(){el('video-list').innerHTML=(DATA.videos||[]).map(v=>`<article class="video-card"><span class="video-play">▶</span><div><span class="tech-pill">${esc(v.platform)} · ${esc(v.topic)}</span><h3>${esc(v.title)}</h3><p>${esc(v.description)}</p><a href="${esc(safeUrl(v.url))}" target="_blank" rel="noopener noreferrer" class="text-button">Abrir conteúdo oficial ↗</a></div></article>`).join('')}
function ensureRecipePage(){
  let root=el('recipe-detail');
  if(root)return root;
  let section=document.querySelector('[data-view="receita"]');
  if(!section){
    section=document.createElement('section');
    section.className='page recipe-detail-page';
    section.dataset.view='receita';
    section.setAttribute('aria-label','Receita completa');
    el('app-main').appendChild(section);
  }
  root=document.createElement('div');
  root.id='recipe-detail';
  section.appendChild(root);
  return root;
}
function goto(page){
const recipeRoute=page.startsWith('receita/');
const recipeId=recipeRoute?page.slice('receita/'.length):null;
if(recipeRoute)ensureRecipePage();
if(recipeRoute)page='receita';
const available=['inicio','receitas','receita','tecnicas','workshops','videos','planejamento'];
if(!available.includes(page))page='inicio';
document.querySelectorAll('[data-view]').forEach(v=>v.classList.toggle('active',v.dataset.view===page));
document.querySelectorAll('[data-page]').forEach(v=>{const active=v.dataset.page===page||(page==='receita'&&v.dataset.page==='receitas');v.classList.toggle('active',active);if(active)v.setAttribute('aria-current','page');else v.removeAttribute('aria-current')});
el('main-nav').classList.remove('open');el('mobile-toggle').setAttribute('aria-expanded','false');
if(page==='receitas')renderRecipes();
if(page==='receita')renderRecipePage(recipeId);
if(page==='planejamento')renderPlanner();
if(page!=='receita')document.title='Dantas Cozinha • um lugar para cozinhar bem';
window.scrollTo(0,0)
}
function fav(id){if(!RECIPES.some(r=>r.id===id))return;if(isFav(id)){state.favorites=state.favorites.filter(x=>x!==id);toast('Removido dos favoritos.')}else{state.favorites.push(id);toast('Receita salva nos favoritos!')}saveState();renderRecipes();renderHome();if(modalRecipe?.id===id && el('recipe-detail-fav'))el('recipe-detail-fav').textContent=isFav(id)?'♥ Salvo':'♡ Salvar receita'}
function qty(n){if(n==null)return '';return Number(n.toFixed(2)).toLocaleString('pt-BR',{maximumFractionDigits:2})}
function ingredientsList(r,factor){
const items=r.ingredients||[];
if(!items.length)return '<li>Esta ficha ainda não possui ingredientes cadastrados.</li>';
let previousGroup='';
return items.map(i=>{
if(typeof i==='string')return `<li class="ingredient-entry"><label class="ingredient-row"><input type="checkbox"><span>${esc(i)}</span></label></li>`;
let section='';
if(i.group && i.group!==previousGroup){section=`<li class="ingredient-group">${esc(i.group)}</li>`;previousGroup=i.group;}
const amount=qty(Number(i.quantity)*factor);
return section+`<li class="ingredient-entry"><label class="ingredient-row"><input type="checkbox"><span><strong class="ingredient-amount">${esc(amount)} ${esc(i.unit)}</strong> de ${esc(i.name)}</span></label></li>`;
}).join('')
}
function openRecipe(id){location.hash='receita/'+encodeURIComponent(id);goto('receita/'+id)}
function renderRecipePage(id){
const r=RECIPES.find(x=>x.id===id),root=ensureRecipePage();
if(!r){root.innerHTML='<div class="shell detail-not-found"><h1>Receita não encontrada</h1><a href="#receitas">Voltar ao catálogo</a></div>';return}
modalRecipe=r;modalServings=Number(r.servings)||1;
document.title=r.title+' • Dantas Cozinha';
root.innerHTML=`<div class="shell detail-shell">
<div class="detail-breadcrumb"><button class="detail-back" type="button" data-goto="receitas">← Todas as receitas</button><span> / </span><span>${esc(categoryName[r.category]||'Receita')}</span></div>
<div class="detail-hero"><figure class="detail-photo">${img(r)}${imageAttribution(r)}</figure>
<div class="detail-intro"><span class="eyebrow">${esc(categoryName[r.category]||'Receita')} · CADERNO DE RECEITAS</span>
<h1>${esc(r.title)}</h1><p>${esc(r.description)}</p>
<div class="detail-stats"><span>◷ ${esc(r.minutesLabel || (r.minutes ? r.minutes+' min' : 'Tempo variável'))}</span><span>✳ ${esc(r.difficulty||'Preparo caseiro')}</span><span>♙ ${esc(r.servingsLabel||(r.servings+' porções'))}</span></div>
<button type="button" id="recipe-detail-fav" class="btn-outline">${isFav(id)?'♥ Salvo':'♡ Salvar receita'}</button></div></div>
<div class="detail-content">
<section class="detail-ingredients"><h2>Ingredientes</h2><p class="detail-subtitle">Marque os itens conforme separá-los.</p>
<div class="serving-control"><span>Rendimento ajustável</span><button type="button" id="serving-minus" aria-label="Diminuir porções">−</button><strong id="serving-number">${esc(modalServings)}</strong><button type="button" id="serving-plus" aria-label="Aumentar porções">+</button></div>
<ul id="ingredients-list">${ingredientsList(r,1)}</ul></section>
<section class="detail-steps"><h2>Modo de preparo</h2><p class="detail-subtitle">Siga as etapas na ordem. As quantidades acima acompanham o rendimento selecionado; o preparo não é recalculado automaticamente.</p><ol>${(r.steps||[]).map(step=>`<li>${esc(step)}</li>`).join('')}</ol></section>
</div>
<div class="detail-extra"><div class="modal-tip">✦ <b>Dica da cozinha:</b> ${esc(r.tip||'Siga as etapas com atenção.')}</div>
${r.recipeVersion?`<p class="recipe-version">${esc(r.recipeVersion)}</p>`:''}
<div class="detail-source"><span class="eyebrow">CRÉDITOS E REFERÊNCIAS</span><p class="recipe-editorial-notice">A referência culinária não significa reprodução literal da receita de terceiros. Consulte a origem indicada para conhecer a publicação original.</p><p>${esc(r.source||r.sourceName||'Receita compartilhada com o Dantas Cozinha')}</p>
${r.sourceUrl?`<a href="${esc(safeUrl(r.sourceUrl))}" target="_blank" rel="noopener noreferrer">Consultar referência: ${esc(r.sourceName||r.source)} ↗</a>`:''}</div>
<div class="modal-notes"><label for="recipe-note">Meu caderno de anotações</label><textarea id="recipe-note" maxlength="5000" placeholder="Como ficou? O que você mudaria?" aria-label="Notas pessoais"></textarea><small>Salvo automaticamente neste navegador.</small></div>
</div></div>`;
el('recipe-note').value=state.notes[id]||'';
el('serving-plus').onclick=()=>scale(1);
el('serving-minus').onclick=()=>scale(-1);
el('recipe-detail-fav').onclick=()=>fav(id);
el('recipe-note').oninput=e=>{state.notes[id]=e.target.value;saveState()};
}
function scale(amount){modalServings=Math.max(1,Math.min(40,modalServings+amount));el('serving-number').textContent=modalServings;el('ingredients-list').innerHTML=ingredientsList(modalRecipe,modalServings/modalRecipe.servings)}

const days=['Seg','Ter','Qua','Qui','Sex','Sáb','Dom'];const meals=[['almoco','Almoço'],['jantar','Jantar']];
function nextEmptySlot(){for(let d=0;d<7;d++)for(const [m] of meals){const k=`${d}-${m}`;if(!state.planner[k])return k}return null}
function quickAdd(id){if(!(RECIPES.find(r=>r.id===id)?.ingredients||[]).length){toast('Esta receita não tem quantidades cadastradas.');return;}let k=nextEmptySlot();if(!k){toast('O cardápio está completo; altere um dia para adicionar.');return}state.planner[k]=id;state.shoppingChecked={};saveState();toast(`Adicionado ao cardápio: ${days[+k[0]]}.`)}
function renderPlanner(){const options=`<option value="">Escolher receita</option>`+RECIPES.map(r=>`<option value="${esc(r.id)}">${esc(r.title)}</option>`).join('');el('week-grid').innerHTML=days.map((d,i)=>`<div class="day-card"><strong>${d}</strong>${meals.map(([code,name])=>`<label for="meal-${i}-${code}">${name}</label><select id="meal-${i}-${code}" data-slot="${i}-${code}">${options}</select>`).join('')}</div>`).join('');document.querySelectorAll('[data-slot]').forEach(s=>s.value=state.planner[s.dataset.slot]||'');renderShopping()}
function grocery(){const sum=new Map();for(const id of Object.values(state.planner)){const r=RECIPES.find(x=>x.id===id);if(!r)continue;for(const i of r.ingredients||[]){if(typeof i==='string')continue;const key=`${i.name.toLocaleLowerCase('pt-BR')}|${i.unit.toLocaleLowerCase('pt-BR')}`;if(!sum.has(key))sum.set(key,{name:i.name,unit:i.unit,quantity:0,key});sum.get(key).quantity+=Number(i.quantity)||0}}return [...sum.values()].sort((a,b)=>a.name.localeCompare(b.name,'pt-BR'))}
function textGrocery(){const list=grocery();return 'DANTAS COZINHA — LISTA DE COMPRAS\n\n'+list.map(i=>`[${state.shoppingChecked[i.key]?'x':' '}] ${qty(i.quantity)} ${i.unit} de ${i.name}`).join('\n')+'\n'}
function renderShopping(){const all=grocery();el('shopping-list').innerHTML=all.length?`<div class="shopping-items">${all.map(i=>`<label class="shopping-item ${state.shoppingChecked[i.key]?'checked':''}"><input type="checkbox" data-shop="${esc(i.key)}" ${state.shoppingChecked[i.key]?'checked':''}><span>${esc(qty(i.quantity))} ${esc(i.unit)} de ${esc(i.name)}</span></label>`).join('')}</div>`:'<div class="shopping-empty">Escolha uma receita no cardápio para gerar a sua lista. 🥕</div>'}
function download(filename,contents,type){const url=URL.createObjectURL(new Blob([contents],{type}));const a=document.createElement('a');a.href=url;a.download=filename;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),2000)}
function doBackup(){download('dantas-cozinha-backup.json',JSON.stringify({app:'dantas-cozinha',version:1,exportedAt:new Date().toISOString(),data:state},null,2),'application/json')}
async function importBackup(file){if(!file)return;try{if(file.size>1_000_000)throw Error('Arquivo muito grande.');const parsed=JSON.parse(await file.text());if(parsed.app!=='dantas-cozinha'||!parsed.data||typeof parsed.data!=='object')throw Error('Formato incompatível.');const s=parsed.data;state={favorites:Array.isArray(s.favorites)?s.favorites.filter(id=>RECIPES.some(r=>r.id===id)):[],notes:s.notes&&typeof s.notes==='object'?s.notes:{},planner:s.planner&&typeof s.planner==='object'?s.planner:{},shoppingChecked:s.shoppingChecked&&typeof s.shoppingChecked==='object'?s.shoppingChecked:{}};saveState();renderHome();renderRecipes();renderPlanner();toast('Backup importado com sucesso!')}catch(e){toast(`Não foi possível importar: ${e.message}`)}}
function initEvents(){window.addEventListener('hashchange',()=>goto(decodeURIComponent(location.hash.slice(1))));document.addEventListener('click',e=>{const go=e.target.closest('[data-goto]');if(go){location.hash=go.dataset.goto;goto(go.dataset.goto);return}const cat=e.target.closest('[data-category-go]');if(cat){selectedFilter=cat.dataset.categoryGo;location.hash='receitas';goto('receitas');return}const f=e.target.closest('[data-fav]');if(f){fav(f.dataset.fav);return}const add=e.target.closest('[data-plan-add]');if(add){quickAdd(add.dataset.planAdd);return}const recipe=e.target.closest('[data-recipe]');if(recipe){openRecipe(recipe.dataset.recipe);return}});
const schoolSearch=el('school-search');if(schoolSearch)schoolSearch.oninput=e=>{selectedSchoolSearch=e.target.value;renderTechniques()};
const schoolFilters=el('school-filters');if(schoolFilters)schoolFilters.onclick=e=>{const button=e.target.closest('[data-school-category]');if(button){selectedSchoolCategory=button.dataset.schoolCategory;renderTechniques()}};
const schoolGrid=el('tech-grid');if(schoolGrid)schoolGrid.onclick=e=>{const link=e.target.closest('[data-school-anchor]');if(link){e.preventDefault();el(link.dataset.schoolAnchor)?.scrollIntoView({behavior:'smooth',block:'start'})}};
el('recipe-search').oninput=e=>{selectedSearch=e.target.value;renderRecipes()};el('recipe-filters').onclick=e=>{const chip=e.target.closest('[data-filter]');if(chip){selectedFilter=chip.dataset.filter;renderRecipes()}};
el('fav-shortcut').onclick=()=>{selectedFilter='favoritas';selectedSearch='';el('recipe-search').value='';location.hash='receitas';goto('receitas')};el('footer-favorites').onclick=el('fav-shortcut').onclick;
el('mobile-toggle').onclick=()=>{const n=el('main-nav');n.classList.toggle('open');el('mobile-toggle').setAttribute('aria-expanded',n.classList.contains('open')?'true':'false')};
el('week-grid').onchange=e=>{const s=e.target.closest('[data-slot]');if(!s)return;if(s.value)state.planner[s.dataset.slot]=s.value;else delete state.planner[s.dataset.slot];state.shoppingChecked={};saveState();renderShopping()};el('shopping-list').onchange=e=>{const b=e.target.closest('[data-shop]');if(!b)return;state.shoppingChecked[b.dataset.shop]=b.checked;saveState();renderShopping()};
el('clear-plan').onclick=()=>{if(!Object.keys(state.planner).length)return;if(confirm('Limpar todo o cardápio desta semana?')){state.planner={};state.shoppingChecked={};saveState();renderPlanner();toast('Cardápio limpo.')}};
el('copy-list').onclick=async()=>{const list=grocery();if(!list.length){toast('Escolha receitas primeiro.');return}try{await navigator.clipboard.writeText(textGrocery());toast('Lista copiada!')}catch{download('lista-de-compras.txt',textGrocery(),'text/plain');toast('Lista salva como arquivo.')}};
el('print-list').onclick=()=>{if(!grocery().length){toast('Escolha receitas primeiro.');return}window.print()};el('export-backup').onclick=doBackup;el('import-backup').onchange=e=>{importBackup(e.target.files?.[0]);e.target.value=''};
}
function main(){updateFavCount();renderHome();renderRecipes();renderCuratedDiscoveries();renderTechniques();renderWorkshops();renderVideos();renderPlanner();initEvents();const last=DATA.generatedAt?new Date(DATA.generatedAt):null;if(last&&!isNaN(last))el('last-update').textContent=`Conteúdo: ${last.toLocaleDateString('pt-BR')}`;goto(decodeURIComponent(location.hash.slice(1))||'inicio')}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',main);else main();
})();
