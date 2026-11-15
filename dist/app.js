const phone = '+18325019594';
const menu = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
menu.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('open', open);
});
navigation.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
  navigation.classList.remove('open');
  menu.setAttribute('aria-expanded', 'false');
}));
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
    navigation.classList.remove('open'); menu.setAttribute('aria-expanded', 'false'); menu.focus();
  }
});
document.querySelectorAll('[data-service]').forEach(a => a.addEventListener('click', () => {
  document.querySelector('#service').value = a.dataset.service;
}));
const form = document.querySelector('#quote-form');
form.addEventListener('submit', e => {
  e.preventDefault();
  if (!form.reportValidity()) return;
  const name = document.querySelector('#customer-name').value.trim();
  const details = document.querySelector('#details').value.trim();
  if (!name || !details) { return; }
  const message = `Hi Ground Line, I'd like an estimate.\n\nName: ${name}\nProperty ZIP: ${document.querySelector('#zip').value}\nService: ${document.querySelector('#service').value}\n\n${details}`;
  document.querySelector('#message-preview').value = message;
  const ios = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  document.querySelector('#send-text').href = `sms:${phone}${ios ? '&' : '?'}body=${encodeURIComponent(message)}`;
  const result = document.querySelector('#message-result');
  result.hidden = false;
  document.querySelector('#copy-status').textContent = '';
  result.scrollIntoView({behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block:'center'});
  document.querySelector('#send-text').focus({preventScroll:true});
});
document.querySelector('#copy-message').addEventListener('click', async () => {
  const text = document.querySelector('#message-preview');
  try {
    await navigator.clipboard.writeText(text.value);
    document.querySelector('#copy-status').textContent = 'Copied. Paste this into a text to (832) 501-9594.';
  } catch {
    text.focus(); text.select();
    document.querySelector('#copy-status').textContent = 'Message selected. Use your device’s Copy command, then paste it into a text.';
  }
});
document.querySelector('#year').textContent = new Date().getFullYear();
