function submitform(){
    frm = $('#infoform');
    frm.submit();
}

function loaduser(){
    $('#firstname').load(' #firstname');
    $('#lastname').load(' #lastname');
    $('#email').load(' #email');
    $('#twitterid').load(' #twitterid');
    $('#website').load(' #website');
    $('#spana').load(' #spana')
}

function loadedit(){
    $('#firstname').load('/edit #firstname');
    $('#lastname').load('/edit #lastname');
    $('#email').load('/edit #email');
    $('#twitterid').load('/edit #twitterid');
    $('#website').load('/edit #website');
    $('#spana').load('/edit #spana')
}
