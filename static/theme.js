(() => {
  const storageKey = 'theme';
  const defaultTheme = 'blue';
  const root = document.documentElement;
  const select = document.getElementById('themeSelect');

  const applyTheme = theme => {
    const value = theme || defaultTheme;
    root.dataset.theme = value;
  };

  const savedTheme = localStorage.getItem(storageKey);
  const initialTheme = savedTheme || defaultTheme;
  applyTheme(initialTheme);

  if (select) {
    select.value = initialTheme;
    select.addEventListener('change', () => {
      const value = select.value || defaultTheme;
      localStorage.setItem(storageKey, value);
      applyTheme(value);
    });
  }
})();
