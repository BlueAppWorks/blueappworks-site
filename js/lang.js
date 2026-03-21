/**
 * Language detection, redirect, and switcher for Blue App Works.
 *
 * - Auto-detects browser language on first visit
 * - Redirects non-Japanese users to /en/
 * - Injects a language switcher into the nav
 * - Stores user preference in localStorage
 */
(function () {
  var STORAGE_KEY = 'baw-lang-pref';
  var path = window.location.pathname;

  // Determine if we're on an English page
  var isEnPage = /\/en\//.test(path) || /\/en$/.test(path);

  // --- Language switcher ---
  var nav = document.getElementById('nav-links');
  if (nav) {
    var switcher = document.createElement('a');
    switcher.className = 'lang-switch';
    if (isEnPage) {
      // On English page: link to Japanese
      var jaPage = path.replace(/\/en\//, '/').replace(/\/en$/, '/');
      if (jaPage === path) jaPage = '/'; // fallback
      switcher.href = jaPage;
      switcher.textContent = 'JP';
      switcher.addEventListener('click', function () {
        localStorage.setItem(STORAGE_KEY, 'ja');
      });
    } else {
      // On Japanese page: link to English
      var enPath = '/en' + (path === '/' ? '/' : path);
      // Handle index.html explicitly
      if (path.endsWith('index.html')) {
        enPath = path.replace('index.html', 'en/index.html');
      } else if (path.endsWith('contact.html')) {
        enPath = path.replace('contact.html', 'en/contact.html');
      } else if (path.endsWith('privacy.html')) {
        enPath = path.replace('privacy.html', 'en/privacy.html');
      } else if (path === '/' || path.endsWith('/')) {
        enPath = path + 'en/';
      }
      switcher.href = enPath;
      switcher.textContent = 'EN';
      switcher.addEventListener('click', function () {
        localStorage.setItem(STORAGE_KEY, 'en');
      });
    }
    // Insert before the CTA button
    var cta = nav.querySelector('.nav-cta');
    if (cta) {
      nav.insertBefore(switcher, cta);
    } else {
      nav.appendChild(switcher);
    }
  }
})();
