(function($) {
    var READ_ONLY = [
        'timestamp'
    ];
    var SERVER = '';

    var $list = $('#bots');

    var setConfiguration = function($bot) {
        var inputThreshold = $bot.find('[data-type="threshold"]').text();
        // var speakerVolume = $bot.find('[data-type="volume"]').text();
        // var state = $bot.find('[data-type="state"] option:selected').val();

        $.ajax({
            url: 'http://localhost:3000',
            method: 'POST',
            data: {
                inputThreshold: ''
            }
        });
    };

    var renderList = function(data) {
        var $template = $('#bots-template');

        var $liClone = $($template[0].content.querySelectorAll('li')).clone();
        // var $selectClone = $($template[0].content.querySelectorAll('select')).clone();
        var $rangeClone = $($template[0].content.querySelectorAll('.range')).clone();

        // Bot name
        var $name = $liClone.find('.bot-name');
        $name.text(data.name);

        // Configuration data
        for (var key in data.configuration) {
            if (data.configuration.hasOwnProperty(key)) {
                var $rowClone = $($template[0].content.querySelectorAll('.row')).clone();

                var $type = $rowClone.find('.type');
                var $value = $rowClone.find('.value');

                var value = data.configuration[key];
                $type.text(key);

                if (key === 'threshold') {
                    $rangeClone.val(value);
                    $value.replaceWith($rangeClone);
                } else {
                    $value.text(value);
                }

                // if (key === 'state') {
                //     $selectClone.find('option').eq(parseInt(value, 10)).attr('selected', 'selected');
                //     $value.replaceWith($selectClone);
                // } else {
                //     $value.text(value);
                // }

                if (READ_ONLY.indexOf(key) !== -1) {
                    $value.attr('readonly', 'readonly');
                    $rowClone.find('.submit').attr('disabled', 'disabled');
                }

                $liClone.find('.info').append($rowClone);
            }
        }

        $list.append($liClone);
    };

    var getBots = function() {
        var $getBotsButton = $('#get-bots');

        $getBotsButton.on('click', function() {
            $.ajax({
                // url: SERVER + '/',
                url: 'http://localhost:3000',
                method: 'GET',
                complete: function(xhr, status) {
                    $list.empty();
                    // var res = JSON.parse(xhr.responseText);

                    var mock = {
                        bots: [
                            {
                                name: 'bot1',
                                configuration: {
                                    timestamp: '13135823058',
                                    threshold: '0.8'
                                }
                            },
                            {
                                name: 'bot2',
                                configuration: {
                                    timestamp: '13135823058',
                                    state: '1'
                                }
                            },
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

        $list.on('click', '.submit', function(evt) {
            var $bot = $(evt.target).parents('.bot');
            setConfiguration($bot);
        });
    };

    var main = function() {
        bindListeners();
    };

    main();
})(window.$);
