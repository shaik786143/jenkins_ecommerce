document.addEventListener("DOMContentLoaded", () => {
    const API_BASE_URL = "http://127.0.0.1:8001/api";

    const totalProductsElem = document.getElementById("total-products");
    const totalSalesElem = document.getElementById("total-sales");
    const totalRevenueElem = document.getElementById("total-revenue");
    const salesTableBody = document.getElementById("sales-table-body");

    // Helper to fetch all pages from a paginated DRF endpoint
    async function fetchAllPages(url) {
        let results = [];
        let nextUrl = url;
        while (nextUrl) {
            const resp = await fetch(nextUrl);
            if (!resp.ok) throw new Error("Network error");
            const data = await resp.json();
            if (Array.isArray(data)) {
                // Unpaginated
                results = data;
                break;
            }
            results = results.concat(data.results);
            nextUrl = data.next;
        }
        return results;
    }

    async function fetchData() {
        try {
            // Fetch all products and sales (all pages)
            const [productsData, salesData] = await Promise.all([
                fetchAllPages(`${API_BASE_URL}/products/`),
                fetchAllPages(`${API_BASE_URL}/sales/`)
            ]);

            productsForCheckout = productsData; // Store products for checkout

            // Create a quick lookup map for sales by product id
            const salesByProduct = {};
            for (const sale of salesData) {
                if (!salesByProduct[sale.product]) salesByProduct[sale.product] = [];
                salesByProduct[sale.product].push(sale);
            }
            // Sort sales for each product by date (most recent first)
            for (const salesArr of Object.values(salesByProduct)) {
                salesArr.sort((a, b) => new Date(b.sale_date) - new Date(a.sale_date));
            }

            updateStats(productsData, salesData);
            populateProductSalesTable(productsData, salesByProduct);

        } catch (error) {
            console.error("Failed to fetch data:", error);
            salesTableBody.innerHTML = `<tr><td colspan="6" style="color: red;">Failed to load data. Is the Django server running?</td></tr>`;
            totalProductsElem.innerText = "Error";
            totalSalesElem.innerText = "Error";
            totalRevenueElem.innerText = "Error";
        }
    }

    function updateStats(products, sales) {
        console.log("[DEBUG] Sales data used for revenue calculation:", sales);
        totalProductsElem.innerText = products.length;
        totalSalesElem.innerText = sales.length;
        const totalRevenue = sales.reduce((sum, sale) => sum + parseFloat(sale.total_price), 0);
        totalRevenueElem.innerText = `$${totalRevenue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }

    function populateProductSalesTable(products, salesByProduct) {
        if (products.length === 0) {
            salesTableBody.innerHTML = '<tr><td colspan="6">No products available.</td></tr>';
            return;
        }
        salesTableBody.innerHTML = "";
        for (const product of products) {
            const row = document.createElement("tr");
            const sales = salesByProduct[product.id] || [];
            if (sales.length > 0) {
                // Show the most recent sale
                const sale = sales[0];
                row.innerHTML = `
                    <td>${product.name}</td>
                    <td>${product.price}</td>
                    <td>${product.inventory}</td>
                    <td>${sale.quantity_sold}</td>
                    <td>$${parseFloat(sale.total_price).toFixed(2)}</td>
                    <td>${new Date(sale.sale_date).toLocaleDateString()}</td>
                `;
            } else {
                // No sales for this product
                row.innerHTML = `
                    <td>${product.name}</td>
                    <td>${product.price}</td>
                    <td>${product.inventory}</td>
                    <td colspan="3" style="color: #aaa; text-align: center;">No sales</td>
                `;
            }
            salesTableBody.appendChild(row);
        }
    }

    // --- Stripe Payment Flow ---
    const stripe = Stripe("pk_test_51RcUZ9EA1AiPn7sI2ahBx3ybez6jW2mpz2a99jl1FnE0AgxvXHgfV6CGqb0UU1LDV9qdqdyA1nykiNnIqbZVyLZG00dL9Nj59F");
    const checkoutButton = document.getElementById("checkout-btn");
    const paymentModal = document.getElementById("payment-modal");
    const paymentForm = document.getElementById("payment-form");
    const paymentHeader = document.getElementById("payment-header");

    let elements;
    let productsForCheckout = []; // Store products to be able to pick one

    // New function to check payment status on page load
    async function checkStatus() {
        const clientSecret = new URLSearchParams(window.location.search).get(
            "payment_intent_client_secret"
        );

        if (!clientSecret) {
            return;
        }

        const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);

        switch (paymentIntent.status) {
            case "succeeded":
                showGlobalMessage("Payment Succeeded! Thank you for your purchase.", "success");
                break;
            case "processing":
                showGlobalMessage("Your payment is processing.", "info");
                break;
            case "requires_payment_method":
                showGlobalMessage("Payment failed. Please try another payment method.", "danger");
                break;
            default:
                showGlobalMessage("Something went wrong.", "danger");
                break;
        }
    }

    checkoutButton.addEventListener("click", async () => {
        // Pick a random product for the checkout demo
        if (productsForCheckout.length === 0) {
            alert("Please wait for products to load before checking out.");
            return;
        }
        const productToCheckout = productsForCheckout[Math.floor(Math.random() * productsForCheckout.length)];
        const amountInCents = Math.round(parseFloat(productToCheckout.price) * 100);

        paymentHeader.innerText = `Checkout: ${productToCheckout.name} - $${productToCheckout.price}`;
        paymentModal.style.display = "block";

        console.log("[DEBUG] Creating payment intent for amount:", amountInCents);
        try {
            const response = await fetch(`${API_BASE_URL}/create-payment-intent/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ amount: amountInCents }),
            });
            const { clientSecret, error } = await response.json();

            if (error) {
                console.error("[DEBUG] Error from backend:", error);
                showMessage(`Error from server: ${error}`);
                return;
            }

            console.log("[DEBUG] Received clientSecret:", clientSecret);

            elements = stripe.elements({ clientSecret });
            const paymentElement = elements.create("payment");
            paymentElement.mount("#payment-element");
        } catch (e) {
            console.error("[DEBUG] Failed to fetch client secret:", e);
            showMessage("Failed to connect to the server.");
        }
    });

    paymentForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        setLoading(true);

        const { error } = await stripe.confirmPayment({
            elements,
            confirmParams: {
                return_url: window.location.href,
            },
        });

        console.error("[DEBUG] Stripe payment error:", error); // Log the full error

        if (error.type === "card_error" || error.type === "validation_error") {
            showMessage(error.message);
        } else {
            showMessage("An unexpected error occurred.");
        }
        setLoading(false);
    });
    
    // Shows a message inside the payment modal
    function showMessage(messageText) {
        const messageContainer = document.querySelector("#payment-message");
        messageContainer.textContent = messageText;
    }

    // Shows a global message at the top of the page
    function showGlobalMessage(messageText, type = "success") {
        const globalAlert = document.getElementById("global-alert");
        globalAlert.className = `alert alert-${type}`;
        globalAlert.textContent = messageText;
        globalAlert.style.display = "block";

        // Clean the URL and hide the message after 5 seconds
        setTimeout(() => {
            globalAlert.style.display = "none";
            window.history.replaceState({}, document.title, window.location.pathname);
        }, 5000);
    }
    
    function setLoading(isLoading) {
        const submitButton = document.querySelector("#submit-payment");
        const buttonText = document.querySelector("#button-text");
        if (isLoading) {
            submitButton.disabled = true;
            buttonText.textContent = "Processing...";
        } else {
            submitButton.disabled = false;
            buttonText.textContent = "Pay now";
        }
    }

    // Run on page load
    checkStatus();

    fetchData();
}); 