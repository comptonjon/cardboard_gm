const searchBtn = document.querySelector('#search-btn');
const body = document.querySelector('body');
searchBtn.addEventListener('click', async function(e) {
    let target = e.target
    e.preventDefault();
    const modal = new ModalWindow().modalWindow;
    body.append(modal);
    const resultsContainer = document.createElement('div')
    resultsContainer.classList.add('results-container');
    modal.append(resultsContainer);
    const query = document.querySelector("#query").value;
    let res = await axios.get('/api/ebay', { params : {'item' : query }})
    if (res.data.length > 0) {
        for (item of res.data) {
        let cell = new EbayCell(item).cell;
        resultsContainer.append(cell);
        }
    } else {
        const noResults = document.createElement('h1');
        noResults.innerText = "NO RESULTS FOUND";
        noResults.classList.add('no-results');
        resultsContainer.append(noResults);
    }

    
    
})
detailBtn.addEventListener('click', function(){
    const modal = new ModalWindow().modalWindow;
    body.append(modal);
    const detailedImage = document.createElement('img');
    detailedImage.classList.add('detail-img')
    detailedImage.setAttribute('src', detailBtn.dataset.url);
    modal.append(detailedImage);
})