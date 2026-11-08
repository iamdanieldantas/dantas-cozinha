import { Capacitor } from '@capacitor/core';
import { Share } from '@capacitor/share';
/* Camada exclusiva do app iOS; não altera o site publicado. */
(() => {
  'use strict';
  const siteUrl = 'https://iamdanieldantas.github.io/dantas-cozinha/';
  const tabs = [
    { id: 'inicio', label: 'Início', icon: '⌂' },
    { id: 'receitas', label: 'Receitas', icon: '▤' },
    { id: 'tecnicas', label: 'Escola', icon: '◈' },
    { id: 'workshops', label: 'Oficinas', icon: '✦' },
    { id: 'planejamento', label: 'Cardápio', icon: '☷' }
  ];

  function notice(message) {
    const node = document.getElementById('toast');
    if (!node) return;
    node.textContent = message;
    node.classList.add('show');
    window.setTimeout(() => node.classList.remove('show'), 2800);
  }

  function currentPage() {
    const path = decodeURIComponent(location.hash.slice(1)).split('/')[0];
    return path === 'receita' ? 'receitas' : path || 'inicio';
  }

  function updateNavigation() {
    const current = currentPage();
    document.querySelectorAll('[data-mobile-tab]').forEach((link) => {
      const active = link.dataset.mobileTab === current;
      link.classList.toggle('active', active);
      if (active) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
  }

  function makeNavigation() {
    const nav = document.createElement('nav');
    nav.className = 'mobile-app-tabs';
    nav.setAttribute('aria-label', 'Navegação do aplicativo');
    for (const tab of tabs) {
      const link = document.createElement('a');
      link.href = '#' + tab.id;
      link.dataset.mobileTab = tab.id;
      link.setAttribute('aria-label', tab.label);
      const icon = document.createElement('span');
      icon.className = 'mobile-tab-icon';
      icon.textContent = tab.icon;
      icon.setAttribute('aria-hidden', 'true');
      const label = document.createElement('span');
      label.className = 'mobile-tab-label';
      label.textContent = tab.label;
      link.append(icon, label);
      nav.appendChild(link);
    }
    document.body.appendChild(nav);
    window.addEventListener('hashchange', updateNavigation);
    updateNavigation();
  }

  async function share(payload) {
    try {
      if (Capacitor.isNativePlatform()) {
        await Share.share(payload);
      } else if (navigator.share) {
        await navigator.share(payload);
      } else if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(payload.url || payload.text);
        notice('Copiado para compartilhar!');
      } else {
        notice('Compartilhamento indisponível neste dispositivo.');
      }
    } catch (error) {
      if (!/cancel/i.test(String(error?.message || error))) {
        notice('Não foi possível compartilhar agora.');
      }
    }
  }

  function insertRecipeShare() {
    const container = document.querySelector('#recipe-detail .detail-intro');
    if (!container || container.querySelector('[data-mobile-recipe-share]')) return;
    const title = container.querySelector('h1')?.textContent?.trim();
    if (!title) return;
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'btn-outline mobile-share-action';
    button.dataset.mobileRecipeShare = '1';
    button.textContent = '↗ Compartilhar receita';
    button.addEventListener('click', () => {
      const id = location.hash.startsWith('#receita/')
        ? decodeURIComponent(location.hash.slice('#receita/'.length))
        : '';
      const url = siteUrl + '#receita/' + encodeURIComponent(id);
      share({ title, text: title + ' — Dantas Cozinha', url });
    });
    container.appendChild(button);
  }

  function insertShoppingShare() {
    const container = document.querySelector('.shopping-buttons');
    if (!container || container.querySelector('[data-mobile-shopping-share]')) return;
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'btn-outline mobile-share-action';
    button.dataset.mobileShoppingShare = '1';
    button.textContent = '↗ Compartilhar lista';
    button.addEventListener('click', () => {
      const lines = [...document.querySelectorAll('#shopping-list .shopping-item span')]
        .map((element) => element.textContent.trim()).filter(Boolean);
      if (!lines.length) {
        notice('Monte um cardápio para gerar sua lista.');
        return;
      }
      share({
        title: 'Lista de compras — Dantas Cozinha',
        text: 'Lista de compras — Dantas Cozinha\n\n' + lines.map((line) => '• ' + line).join('\n')
      });
    });
    container.appendChild(button);
  }

  function setupConnectivityNotice() {
    const message = document.createElement('div');
    message.className = 'mobile-offline-notice';
    message.setAttribute('role', 'status');
    message.textContent = 'Sem internet: receitas e aulas do app continuam disponíveis. Imagens e links externos podem não abrir.';
    document.body.appendChild(message);
    const update = () => message.classList.toggle('visible', !navigator.onLine);
    window.addEventListener('offline', update);
    window.addEventListener('online', update);
    update();
  }

  function init() {
    document.body.classList.add('mobile-app');
    makeNavigation();
    setupConnectivityNotice();
    insertShoppingShare();
    const root = document.getElementById('recipe-detail');
    if (root) {
      new MutationObserver(insertRecipeShare).observe(root, { childList: true });
      insertRecipeShare();
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
