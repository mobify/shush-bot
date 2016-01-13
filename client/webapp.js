(function($) {
    var READ_ONLY = [
        'timestamp'
    ];
    var SERVER = 'http://localhost:3000';

    var $list = $('#bots');

    var setConfiguration = function($bot) {
        var inputThreshold = $bot.find('.range input').val();
        // var speakerVolume = $bot.find('[data-type="volume"]').text();
        // var state = $bot.find('[data-type="state"] option:selected').val();

        $.ajax({
            url: SERVER,
            method: 'POST',
            data: {
                inputThreshold: inputThreshold
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
                    $rangeClone.find('input').val(value);
                    $value.replaceWith($rangeClone);
                } else {
                    $value.val(value);
                }

                // if (key === 'state') {
                //     $selectClone.find('option').eq(parseInt(value, 10)).attr('selected', 'selected');
                //     $value.replaceWith($selectClone);
                // } else {
                //     $value.text(value);
                // }

                if (READ_ONLY.indexOf(key) !== -1) {
                    $value.attr('readonly', 'readonly');
                    $rowClone.find('.submit').addClass('hidden');
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
                url: SERVER,
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
                                    threshold: '-30'
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
