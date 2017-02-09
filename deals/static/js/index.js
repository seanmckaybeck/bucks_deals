function percentage_changed() {
    var percentage = parseInt($('#bucks-percent')[0].value) / 100;
    $('.item').each(function(idx){
        var kids = $(this).children();
        kids[5].textContent = (kids[3].textContent * prices[kids[2].textContent.toLowerCase()]).toFixed(2); // melt: weight * spot
        kids[6].textContent = (kids[4].textContent * percentage).toFixed(2); // bucks: price * bucks percentage
        if (kids[6].textContent > 100)
            kids[6].textContent = 100;
        kids[7].textContent = (kids[4].textContent - kids[5].textContent - kids[6].textContent).toFixed(2); // melt difference with bucks: price - melt - bucks
        if (kids[7].textContent >= 0)
            kids[7].setAttribute('bgcolor', 'crimson');
        else
            kids[7].setAttribute('bgcolor', 'limegreen');
        kids[8].textContent = (kids[4].textContent * 0.02).toFixed(2); // 2% cashback cc: price * 0.02
        kids[9].textContent = (kids[4].textContent - kids[5].textContent - kids[6].textContent - kids[8].textContent).toFixed(2); // melt difference with bucks and cashback: price - melt - bucks - cashback
        if (kids[9].textContent >= 0)
            kids[9].setAttribute('bgcolor', 'crimson');
        else
            kids[9].setAttribute('bgcolor', 'limegreen');
        kids[10].textContent = (kids[6].textContent / kids[3].textContent).toFixed(2); // bucks/ozt: bucks / weight
    });
    var table = $('item-table');
    sorttable.makeSortable(table);
}
