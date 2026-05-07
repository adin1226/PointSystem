
//處理JWT太快過期
function getAccessToken() {
    return localStorage.getItem("access");
}


async function refreshToken() {

    const refresh = localStorage.getItem("refresh");

    const res = await fetch("/api/users/token/refresh/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            refresh: refresh
        })
    });

    const data = await res.json();

    if (data.access) {
        localStorage.setItem("access", data.access);
        return data.access;
    } else {
        logout();
    }
}


async function authFetch(url, options = {}) {

    let token = getAccessToken();

    options.headers = {
        ...options.headers,
        "Authorization": "Bearer " + token
    };

    let res = await fetch(url, options);

    // 🔥 token 過期 → 自動 refresh
    if (res.status === 401) {

        token = await refreshToken();

        options.headers["Authorization"] = "Bearer " + token;

        res = await fetch(url, options);
    }

    return res;
}


function logout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    window.location.href = "/api/users/login-page/";
}