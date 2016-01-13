(function($) {
    var READ_ONLY = [
        'timestamp'
    ];
    var SERVER = '';

    var $list = $('#bots');

    var setConfiguration = function() {

    };

    var renderList = function(data) {
        var $template = $('#bots-template');

        var $clone = $($template[0].content.querySelectorAll('li')).clone();

        var $name = $clone.find('.bot-name');
        var $info = $clone.find('.info');

        $name.text(data.name);
        $info.find('.type').text(data.type);
        $info.find('.data').text(data.data);

        if (READ_ONLY.indexOf(data.type) !== -1) {
            $info.find('.data').attr('readonly', 'readonly');
            $info.find('.submit').attr('disabled', 'disabled');
        }

        $list.append($clone);
    };

    var getBots = function() {
        var $getBotsButton = $('#get-bots');

        $getBotsButton.on('click', function() {
            $.ajax({
                // url: SERVER + '/',
                url: 'http://localhost:3000',
                complete: function(xhr, status) {
                    $list.empty();
                    // var res = JSON.parse(xhr.responseText);

                    var mock = {
                        bots: [
                            {
                                name: 'bot1',
                                type: 'timestamp',
                                info: '13135823058'
                            },
                            {
                                name: 'bot2'
                            }
                        ]
                    };

                    $.each(mock.bots, function(idx, bot) {
                        renderList(bot);
                    });
                }
            });
        });
    };

    var bindListeners = function() {
        getBots();
    };

    var main = function() {
        bindListeners();
    };

    main();
})(window.$);
