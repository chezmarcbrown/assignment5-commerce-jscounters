document.addEventListener('DOMContentLoaded', ()=> {
    update_counters();
    setInterval(update_counters, 5000);
});
 
function update_counters() {
    fetch("/api/get_counters")
    .then(response => response.json())
    .then(data => {
        update_innerHTML('#active_counter', data['all_listings_count'])
        update_innerHTML('#watchlist_counter', data['my_watchlist_count'])
    })
    .catch(error => {
        console.log('**** api/counters error **', error);
    });
}

function update_innerHTML(element_id, value) {
    if (document.querySelector(element_id) != undefined) {
        document.querySelector(element_id).innerHTML = value;
    }
}