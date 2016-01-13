(function($) {
    var server = '';

    var setConfiguration = function() {

    };

    var getBots = function() {
        var $getBotsButton = $('#get-bots');
        var $template = $('#bots-template');
        var $list = $('#bots');

        var renderRow = function(data) {
            var $clone = $($template[0].content.querySelectorAll('li')).clone();
            var $name = $clone.find('.header');

            $name.text(data.name);
            $list.append($clone);
        };

        $getBotsButton.on('click', function() {
            $.ajax({
                // url: server + '/',
                url: 'http://localhost:3000',
                complete: function(xhr, status) {
                    $list.empty();
                    // var res = JSON.parse(xhr.responseText);

                    var mock = {
                        bots: [
                            {
                                name: 'hello'
                            },
                            {
                                name: 'world'
                            }
                        ]
                    };

                    $.each(mock.bots, function(idx, bot) {
                        renderRow(bot);
                    });
                }
            });
        });
    };

    var populateBotList = function() {

    };

    var bindListeners = function() {
        getBots();
    };

    var main = function() {
        bindListeners();
    };

    main();
})(window.$);
