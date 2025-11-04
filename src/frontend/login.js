(function () {
  const apiBase = "/api/v1";

  const els = {
    form: document.getElementById("login-form"),
    identifier: document.getElementById("identifier"),
    password: document.getElementById("password"),
    loginError: document.getElementById("login-error"),
    accessOut: document.getElementById("access-token"),
    refreshOut: document.getElementById("refresh-token"),
    actionError: document.getElementById("action-error"),
    logoutBtn: document.getElementById("logout-btn"),
    refreshBtn: document.getElementById("refresh-btn"),
  };

  function setTokens(accessToken, refreshToken) {
    if (accessToken) localStorage.setItem("access_token", accessToken);
    if (refreshToken) localStorage.setItem("refresh_token", refreshToken);
    renderTokens();
  }

  function getTokens() {
    return {
      access: localStorage.getItem("access_token") || "",
      refresh: localStorage.getItem("refresh_token") || "",
    };
  }

  function renderTokens() {
    const { access, refresh } = getTokens();
    els.accessOut.textContent = access || "";
    els.refreshOut.textContent = refresh || "";
  }

  async function login(identifier, password) {
    const res = await fetch(`${apiBase}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ identifier, password }),
    });
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.detail || `Login failed (${res.status})`);
    }
    return res.json();
  }

  async function logout() {
    const { access } = getTokens();
    if (!access) throw new Error("No access token present");
    const res = await fetch(`${apiBase}/auth/logout/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token: access }),
    });
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.detail || `Logout failed (${res.status})`);
    }
    return res.json();
  }

  async function refresh() {
    const { refresh } = getTokens();
    if (!refresh) throw new Error("No refresh token present");
    const res = await fetch(`${apiBase}/auth/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refresh }),
    });
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.detail || `Refresh failed (${res.status})`);
    }
    return res.json();
  }

  // Wire form
  els.form.addEventListener("submit", async (e) => {
    e.preventDefault();
    els.loginError.textContent = "";
    els.actionError.textContent = "";
    try {
      const data = await login(els.identifier.value.trim(), els.password.value);
      const access = data?.access_token?.access_token || "";
      const newRefresh = data?.refresh_token || "";
      setTokens(access, newRefresh);
    } catch (err) {
      els.loginError.textContent = err.message || String(err);
    }
  });

  // Logout
  els.logoutBtn.addEventListener("click", async () => {
    els.actionError.textContent = "";
    try {
      await logout();
      setTokens("", "");
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      renderTokens();
    } catch (err) {
      els.actionError.textContent = err.message || String(err);
    }
  });

  // Refresh access token
  els.refreshBtn.addEventListener("click", async () => {
    els.actionError.textContent = "";
    try {
      const data = await refresh();
      const access = data?.access_token?.access_token || "";
      const newRefresh = data?.refresh_token || "";
      setTokens(access, newRefresh);
    } catch (err) {
      els.actionError.textContent = err.message || String(err);
    }
  });

  // Initial
  renderTokens();
})();



