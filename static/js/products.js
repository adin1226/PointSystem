function openProductModal() {
    const modal = new bootstrap.Modal(document.getElementById('productModal'));
    modal.show();
}

async function createProduct() {
    const token = localStorage.getItem("access");

    const res = await fetch("/api/products/create/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
            name: document.getElementById("productName").value,
            points_required: document.getElementById("productPoints").value,
            stock: document.getElementById("productStocks").value
        })
    });

    const data = await res.json();

    if (res.ok) {
        alert("商品刊登成功");
        location.reload();
    } else {
        alert(data.error || "刊登失敗");
    }
}

function showProductModal() {
    const token = localStorage.getItem("access");

    if (!token) {
        alert("請先登入");
        return;
    }
    
    loadMerchantProducts();

    const modal = new bootstrap.Modal(document.getElementById('showProductModal'));
    modal.show();
}

async function loadMerchantProducts() {

    const token = localStorage.getItem("access");

    const res = await fetch("/api/products/merchant", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    const data = await res.json();

    const container = document.getElementById("productList");
    const empty = document.getElementById("emptyState");

    container.innerHTML = "";

    if (data.length === 0) {
        empty.style.display = "block";
        return;
    }

    empty.style.display = "none";

    data.forEach(p => {
        container.innerHTML += `
        <div class="col-12 mb-2">
          <div class="card">

            <div class="card-body">

              <h5>${p.name}</h5>

              <div class="d-flex gap-2">
                <input type="number"
                       id="stock-${p.id}"
                       value="${p.stock}"
                       class="form-control form-control-sm"
                       placeholder="數量">
                <input type="number"
                       id="points-${p.id}"
                       value="${p.points_required}"
                       class="form-control form-control-sm"
                       placeholder="點數">

                <button class="btn btn-sm btn-primary"
                        onclick="updateProduct(${p.id})">
                    更新
                </button>

                <button class="btn btn-sm btn-danger"
                        onclick="deleteProduct(${p.id})">
                    下架
                </button>
              </div>

            </div>

          </div>
        </div>
        `;
    });
}

async function updateProduct(id) {

    const token = localStorage.getItem("access");

    const stock = document.getElementById(`stock-${id}`).value;

    const points_required = document.getElementById(`points-${id}`).value;

    const res = await fetch(`/api/products/${id}/update/`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
            stock: Number(stock),
            points_required: Number(points_required)
        })
    });

    const data = await res.json();

    if (res.ok) {
        alert("更新成功");
        loadMerchantProducts(); // 🔥 重新刷新列表
    } else {
        alert(data.error || "更新失敗");
    }
}


async function deleteProduct(id) {

    const token = localStorage.getItem("access");

    const res = await fetch(`/api/products/${id}/delete/`, {
        method: "DELETE",
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    const data = await res.json();

    if (res.ok) {
        alert("已下架");
        loadMerchantProducts(); // 🔥 重新載入列表
    } else {
        alert(data.error || "下架失敗");
    }
}