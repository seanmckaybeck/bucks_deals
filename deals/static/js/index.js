function set_color(tag) {
    if (tag.textContent >= 0)
        tag.setAttribute('bgcolor', 'crimson');
    else
        tag.setAttribute('bgcolor', 'limegreen');
}


function percentage_changed() {
    var bucks = parseInt($('#bucks-percent')[0].value) / 100;
    var cashback = parseFloat($('#cash-percent')[0].value) / 100;
    $('.item').each(function(idx){
        var kids = $(this).children();
        kids[5].textContent = (kids[3].textContent * prices[kids[2].textContent.toLowerCase()]).toFixed(2); // melt: weight * spot
        kids[6].textContent = (kids[4].textContent * bucks).toFixed(2); // bucks: price * bucks percentage
        if (kids[6].textContent > 100)
            kids[6].textContent = 100;
        kids[7].textContent = (kids[4].textContent - kids[5].textContent - kids[6].textContent).toFixed(2); // melt difference with bucks: price - melt - bucks
        set_color(kids[7]);
        kids[8].textContent = ((kids[7].textContent / kids[5].textContent) * 100).toFixed(2); // % melt diff = meltdiff / melt * 100
        set_color(kids[8]);
        kids[9].textContent = (kids[4].textContent * cashback).toFixed(2); // x% cashback cc: price * cashback percentage
        kids[10].textContent = (kids[4].textContent - kids[5].textContent - kids[6].textContent - kids[9].textContent).toFixed(2); // melt difference with bucks and cashback: price - melt - bucks - cashback
        set_color(kids[10]);
        kids[11].textContent = ((kids[10].textContent / kids[5].textContent) * 100).toFixed(2); // % melt cash diff = meltcashdiff / melt * 100
        set_color(kids[11]);
        kids[12].textContent = (kids[6].textContent / kids[3].textContent).toFixed(2); // bucks/ozt: bucks / weight
    });
    $('#item-table').tablesorter();
    // var table = $('#item-table')[0];
    // sorttable.makeSortable(table);
}

/*
function toggle_columns(checkbox) {
    if (checkbox.is(':checked')) {
        $('.percent').show();
        $('.dollars').hide();
    }
    else {
        $('.percent').hide();
        $('.dollars').show();
    }
}


function pageload() {
    percentage_changed();
    toggle_columns($($('#toggle')[0]));
}
*/
