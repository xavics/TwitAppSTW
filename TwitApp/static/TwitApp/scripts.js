function submitform(){
    frm = $('#infoform');
    frm.submit();
}

function loaduser(){
    $('#buttons_profile').load(' #buttons_profile');
    $('#name').load(' #name');
    $('#email').load(' #email');
    $('#twitterid').load(' #twitterid');
    $('#website').load(' #website');
    $('#country').load(' #country');
    $('#map').load(' #map');
    $('#region').load(' #region');
    $('#location').load(' #location');
    $('#street').load(' #street');
    $('#postalCode').load(' #postalCode');
}

function loadedit(){
    $('#buttons_profile').load('/edit #buttons_profile');
    $('#name').load('/edit #name');
    $('#email').load('/edit #email');
    $('#twitterid').load('/edit #twitterid');
    $('#website').load('/edit #website');
    $('#country').load('/edit #country');
    $('#region').load('/edit #region');
    $('#location').load('/edit #location');
    $('#street').load('/edit #street');
    $('#postalCode').load('/edit #postalCode');
}

function search(input, tag, id) {
    var x;
    var text;
    for (x=0; x<document.getElementById(id).children.length; x++){
        text = document.getElementById(id).children[x].getElementsByTagName(tag)[0].innerHTML;
        if (text.search(input.value) == -1)
            document.getElementById(id).children[x].style.display = 'none';
        else
            document.getElementById(id).children[x].style.display = 'block';
    }
}

function obtain_twits_user(input, url){
    var data;
    data = $(input).attr("data");
    $.ajax({
        url: url,
        data: {'data':data},
        success: function (data) {
            $('#content-center-twit-search').html(data);
        }
    });
}


function savetweet(input){
    var tweet;
    tweet = $(input).attr("tweet");
    $.ajax({
        url: '/save_tweet',
        data: {'tweet': tweet},
        success: function (data) {
            input.innerHTML = data;
            input.style.color = "red";
            input.style.cursor = "pointer";
            input.setAttribute("tweet", tweet);
            input.setAttribute("onclick", "deletetweet(this,'search')")
        }
    });
}

function deletetweet(input, type){
    var tweet;
    tweet = $(input).attr("tweet");
    $.ajax({
        url: '/delete_tweet',
        data: {'tweet': tweet, 'type': type},
        success: function (data) {
            if(type == 'myTwits') {
                location.reload();
            }else {
                input.innerHTML = data;
                input.style.color = "green";
                input.style.cursor = "pointer";
                input.setAttribute("onclick", "savetweet(this)")
            }
        }
    });
}


function savefavorite(input){
    var screenname;
    screenname = $(input).attr("data");
    $.ajax({
        url: '/add_favorites',
        data: {'screenname':screenname},
        success: function (data) {
            input.innerHTML = data;
            input.style.color = "red";
            input.style.cursor = "pointer";
            input.setAttribute("data", screenname);
            input.setAttribute("onclick", "deletefavorite(this,'search')")
        }

    });
}

function deletefavorite(input, type){
    var screenname;
    screenname = $(input).attr("data");
    $.ajax({
        url: '/delete_favorites',
        data: {'screenname':screenname,
                'type': type},
        success: function (data) {
            if(data == "deleted") {
                location.reload();
            }else{
                input.innerHTML = data;
                input.style.color = "blue";
                input.style.cursor = "pointer";
                input.setAttribute("data", screenname);
                input.setAttribute("onclick", "savefavorite(this)")
            }
        }
    });
}

function searchTrendy(input, img, count_id, option_id){
    $(img).show();
    var query;
    var dict;
    var option;
    var count;
    count = document.getElementById(count_id).value;
    if(count > 80 || count < 1 && count != ''){
        $(img).hide();
        return window.alert("Min/Max Count = 1/80");
    }
    if(count == ''){
        count = 20;
    }
    if(option_id){
        option = document.getElementById(option_id);
    }
    if(input.hasAttribute("data")) {
        query = $(input).attr("data");
        dict = {'query': query, 'count': count}
    }
    else
    {
        if(option.checked == true) {
            query = document.getElementById($(input).attr("inputsubmit")).value;
            if(query == ''){
                $(img).hide();
                return window.alert("Input empty");
            }else {
                for(l in query){
                    if (!query[l].match(/^[a-zA-Z0-9]+$/)){
                        $(img).hide();
                        return window.alert("Users have only letters and numbers");
                    }
                }
                dict = {'screen_user': query, 'count': count}
            }
        }else{
            query = document.getElementById($(input).attr("inputsubmit")).value;
            if(query == ''){
                $(img).hide();
                return window.alert("Input empty");
            }else {
                dict = {'query': query, 'count': count}
            }
        }
    }
    $.ajax({
        url: '/search',
        data: dict,
        success: function (data) {
            $('#content-center-twit-search').html(data);
            $(img).hide()
        }
    });
}

function ajaxPetition(input){
    var data;
    data = $(input).attr("data");
    $.ajax({
        url: '/user_twitter_view',
        data: {'data':data},
        success: function (data) {
            $('body').append(data);
            $('body').css("overflow","hidden");
        }
    });
}

function removeHtml(input){
    $(input).remove()
    $('body').css("overflow","auto");
}

function radioSwitch(change){
    var radio = document.getElementById(change);
    radio.checked = false;
}

function reload_autocomplete() {
    $(function () {
        $("#location_auto").autocomplete({
            source: function (request, response) {
                $.ajax({
                    url: "http://ws.geonames.org/searchJSON",
                    dataType: "jsonp",
                    data: {
                        featureClass: "P",
                        maxRows: 10,
                        name_startsWith: request.term,
                        username: "xavics"
                    },
                    success: function (data) {
                        response($.map(data.geonames, function (item) {
                            return {
                                label: item.name + (item.adminName1 ? ", " + item.adminName1 : "") + ", " + item.countryName,
                                value: item.name,
                                stateOrProvince: item.adminName1,
                                countryName: item.countryName
                            }
                        }));
                    }
                });
            },
            minLength: 2,
            select: function (event, ui) {
                if (ui.item) {
                    $("#id_stateOrProvince").val(ui.item.stateOrProvince);
                    $("#id_country").val(ui.item.countryName);
                    $("#id_zipCode").val("");
                }
            }
        });
    });
}