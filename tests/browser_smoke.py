from playwright.sync_api import sync_playwright
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from weekly_update import load
import http.server,socketserver,threading,os,time
root=Path(__file__).resolve().parents[1]
os.chdir(root)
class Handler(http.server.SimpleHTTPRequestHandler):
  def log_message(self,*args):pass
with socketserver.TCPServer(('127.0.0.1',0),Handler) as server:
  threading.Thread(target=server.serve_forever,daemon=True).start()
  recipes=load(root/'assets/data.js')['recipes']
  html=(root/'index.html').read_text(encoding='utf-8')
  html=html.replace('<link rel="stylesheet" href="assets/styles.css">','<style>'+ (root/'assets/styles.css').read_text(encoding='utf-8') +'</style>')
  html=html.replace('<script defer src="assets/data.js"></script>', '<script>'+ (root/'assets/data.js').read_text(encoding='utf-8') +'</script>')
  html=html.replace('<script defer src="assets/app.js"></script>', '<script>'+ (root/'assets/app.js').read_text(encoding='utf-8') +'</script>')
  with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1440,'height':900},device_scale_factor=1)
    errs=[]
    page.on('pageerror',lambda e:errs.append(str(e)))
    page.set_content(html,wait_until='domcontentloaded')
    page.screenshot(path=str(root/'preview-desktop.png'),full_page=True)
    assert page.locator('#home-recipes .recipe-card').count()==3, f'Home cards: {page.locator(".recipe-card").count()}'
    page.click('[data-goto="receitas"]')
    assert page.locator('#recipe-list .recipe-card').count()==len(recipes)
    page.fill('#recipe-search','brownie')
    assert page.locator('#recipe-list .recipe-card').count()>=2
    page.click('#recipe-list [data-recipe="curadoria-brownie"]')
    assert page.locator('#recipe-dialog').is_visible()
    page.click('#serving-plus')
    assert page.locator('#serving-number').inner_text()=='13'
    page.fill('#recipe-note','Usei chocolate 60%.')
    page.click('#modal-close')
    page.fill('#recipe-search','')
    page.click('#recipe-list [data-fav="curadoria-brownie"]')
    assert page.locator('#fav-count').inner_text()=='1'
    page.click('#recipe-list [data-plan-add="curadoria-brownie"]')
    print('BEFORE', page.evaluate('location.href'), page.evaluate('JSON.stringify({planner:document.querySelector("#week-grid")?.children.length, cards:document.querySelectorAll("#shopping-list .shopping-item").length})'))
    page.click('#main-nav [data-page="planejamento"]')
    print('AFTER',page.evaluate('location.href'), page.locator('#week-grid').count(), page.locator('#shopping-list').count(),page.locator('#shopping-list').inner_text()[:200])
    assert page.locator('#shopping-list .shopping-item').count()==0, 'Não inventar ingredientes ou quantidades'
    assert page.locator('#meal-0-almoco').input_value()=='', 'Ficha sem medidas não entra no planejador'
    page.click('#export-backup')
    # mobile
    mobile=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True)
    mobile.on('pageerror',lambda e:errs.append('mobile: '+str(e)))
    mobile.set_content(html,wait_until='domcontentloaded')
    mobile.screenshot(path=str(root/'preview-mobile.png'),full_page=True)
    assert mobile.locator('.mobile-toggle').is_visible()
    mobile.click('#mobile-toggle')
    assert mobile.locator('#main-nav').is_visible()
    mobile.click('#main-nav a[data-page="workshops"]')
    assert mobile.locator('#workshop-list .workshop-card').count()>=3
    assert not errs, errs
    print('SMOKE OK: receitas/busca/detalhes/escala/notas/favoritos/proteção contra quantidades fictícias/backup/navegação mobile')
    print('Desktop screenshot:',(root/'preview-desktop.png').stat().st_size,'bytes')
    print('Mobile screenshot:',(root/'preview-mobile.png').stat().st_size,'bytes')
    browser.close()
  server.shutdown()
