let isLoading = false;
let length = 10;
let offset = 0;


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function fetchProducts() {
    isLoading = true;
    const token = await getCookie('token');
    if (!token) {
        console.error('No token found in cookies');
        return;
    }

    try {
        const response = await fetch(`/api/products/?length=${length}&offset=${offset}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch products: ${response.statusText}`);
        }
        offset+=length

        const products = await response.json();
        populateProducts(products);
    } catch (error) {
        console.error('Error:', error.message);
    } finally {
        // loader.style.display = 'none';
        isLoading = false;
    }
}

function populateProducts(products) {
    const productContainer = document.querySelector('.pro-container')
    const productTemplate = document.querySelector('#product-template');

    products.forEach(product => {
        const productElement = productTemplate.content.cloneNode(true);
        productElement.querySelector('.product-image').src = product.image;
        productElement.querySelector('.product-category').textContent = product.category;
        productElement.querySelector('.product-name').textContent = product.name;
        productElement.querySelector('.product-price').textContent = product.price;
        // productElement.querySelector('.product-favorite')
        productContainer.appendChild(productElement);
    });
}

const observer = new IntersectionObserver(
    async (entries) => {
      if (entries[0].isIntersecting && !isLoading) {
        await sleep(500);
        await fetchProducts();
      }
    },
    {
      root: null, // Use the viewport as the root
      rootMargin: '0px',
      threshold: 1.0, // Trigger when the loader is fully visible
    }
  );
  
  // Start observing the loader
  

async function main() {
    const target = document.querySelector('#pagination');
    observer.observe(target);
    await fetchProducts()
}


document.addEventListener('DOMContentLoaded', main);
