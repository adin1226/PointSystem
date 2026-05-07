// 顯示點數使用紀錄
function showPointsInfo() {

    const access = localStorage.getItem("access");

    if (!access) {
        alert("請先登入才能查看點數");
        return;
    }

    fetch("/api/users/now/", {
        headers: {
            "Authorization": "Bearer " + access
        }
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("pointsValue").innerText = data.points;
    });


    fetch("/api/member_transactions", {
        method: "GET",
        headers: {
            "Authorization": "Bearer " + access
        }
    })
    .then(res => res.json())
    .then(data => {

        const list = document.getElementById("transactionList");
        list.innerHTML = "";

        if (data.length === 0) {
            list.innerHTML = `<li class="list-group-item text-muted">尚無交易紀錄</li>`;
            return;
        }

        data.forEach(tx => {
            const item = document.createElement("li");
            item.className = "list-group-item";

            item.innerText = `
                商品: ${tx.product_name || tx.product} 
                使用點數: ${tx.points_used}
                時間: ${new Date(tx.created_at).toLocaleString('zh-TW') || ""}
                            `;

            list.appendChild(item);
        });

    })
    .catch(err => {
        console.error(err);
    });

    const modal = new bootstrap.Modal(document.getElementById('pointsModal'));
    modal.show();
}

async function deposit() {
    console.log("token:", localStorage.getItem("access"));
    const token = localStorage.getItem("access");


    const amountInput = document.getElementById("depositAmount");
    const amount = parseInt(amountInput.value);

    const res = await authFetch("/api/users/deposit/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ amount: amount })
    });

    const data = await res.json();

    if (res.ok) {
        alert("儲值成功：" + data.points);
        document.getElementById("pointsValue").innerText = data.points;
        amountInput.value = "";
    } else {
        alert(data.error);
    }
}