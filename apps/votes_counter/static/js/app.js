_slgf = slugify
slugify = function(str) {
    return _slgf(str).toLowerCase();
};

let app = {
    candidates: {},
    votes: {
        total: 0,
        candidates: {},
        pollingPlaces: {},
        pollingPlacesTables: {}
    },
    current: {
        comuna: null,
        pollingPlace: null,
        pollingPlaceTable: null,
        votesInChange: {},
        addVotesInChange: function(id, value) {
            this.votesInChange[id] = value;
            this._localStorageVotesInChange();
        },
        removeVotesInChange: function(id) {
            delete this.votesInChange[id];
            this._localStorageVotesInChange();
        },
        localStorageChanges: function(){
            let votesJSON = localStorage.getItem('pending-changes'),
                locationJSON = localStorage.getItem('pending-changes-location'),
                pendings = null
            ;

            if(votesJSON)
                pendings = {
                    "location": JSON.parse(locationJSON),
                    "votes": JSON.parse(votesJSON)
                };

            return pendings
        },
        clearVotesInChange: function(ask) {
            let go = true,
                pendings = this.localStorageChanges()
            ;

            if(pendings && (!jQuery.isEmptyObject(pendings.votes)) && typeof(ask) !== "undefined" && ask)
                go = confirm('Hay un conjunto de cambios sin guardar, ¿Desea descartar los cambios?');

            if(go) {
                this.votesInChange = {};
                this._localStorageVotesInChange();
            }

            return go
        },
        _localStorageVotesInChange: function() {
            if($.isEmptyObject(this.votesInChange)) {
                localStorage.removeItem('pending-changes');
                localStorage.removeItem('pending-changes-location');
            } else {
                localStorage.setItem('pending-changes', JSON.stringify(this.votesInChange));
                localStorage.setItem('pending-changes-location', JSON.stringify({
                    "comuna": this["comuna"],
                    "pollingPlace": this["pollingPlace"],
                    "pollingPlaceTable": this["pollingPlaceTable"],
                }));
            }
        }
    },
    checkPendingVotes: function() {
        let pendings = this.current.localStorageChanges();
        if(!pendings || $.isEmptyObject(pendings.votes))
            return;

        this.recover = pendings;
    },
    recover: null,
    votesWatcherLock: false,
    votesWatcherTimeout: null,
    opsQueue: [],
    votesWorkerInterval: 2000,
    _votesWatcher: function() {
        if(app.opsQueue.length)
            app.processQueue();
        else if(app.current.comuna)
            app.loadPollingPlaceTableVotes(
                app.current.comuna,
                app.current.pollingPlace,
                app.current.pollingPlaceTable,
                false
            );

        if(!app.votesWatcherLock)
            app.votesWatcherTimeout = setTimeout(app._votesWatcher, app.votesWorkerInterval);

    },
    startVotesWatcher: function() {
        app.votesWatcherLock = false;
        app._votesWatcher();
    },
    stopVotesWatcher: function() {
        if(app.votesWatcherTimeout)
            clearTimeout(app.watcherTimeout);

        app.votesWatcherLock = true;
        app.watcherTimeout = null;
    },
    processQueue: function() {
        let opsJson = [];

        while(this.opsQueue.length !== 0)
            opsJson.push(this.opsQueue.pop());

        $.ajax({
            type: 'POST',
            url: (
                '/api/comunas/' + app.current.comuna
                + '/polling-places/' + app.current.pollingPlace
                + '/tables/' + app.current.pollingPlaceTable + '/votes/'
            ),
            data: JSON.stringify(opsJson),
            contentType: "application/json",
            dataType: 'json'
        })
            .done(app._votesCallback)
            .fail(app.unblock)
        ;

    },
    jsonOp: function(op, cant, candidate) {
        return {"op": op, "cant": cant, "candidate": candidate};
    },
    ops: {
        "add": (a, b) => a + b,
        "remove": (a, b) => a - b
    },
    loadCandidates: function(callback) {
        if(typeof(callback) === "undefined")
            callback = false;

        $.getJSON(
            '/api/candidates/', function(candidates) {
                app.candidates = candidates;
                if(callback)
                    callback();
            }
        )
    },
    loadLists: function(callback) {
        if(typeof(callback) === "undefined")
            callback = false;

        $.getJSON(
            '/api/lists/', function(lists) {
                app.lists = lists;
                if(callback)
                    callback();
            }
        )
    },
    loadDashboardVotes: function() {
        $.getJSON(
            '/api/dashboard/votes/', function(votes) {
                app.votes.total = 0;
                app.votes.lists = {};

                $.each(app.candidates, function(candidate, config) {
                    app.votes.candidates[slugify(candidate)] = 0;
                });

                $.each(votes, function(comuna, comunaVotes) {
                    $.each(comunaVotes, function(pollingPlace, pollingPlaceVotes) {
                        app.votes.pollingPlaces[pollingPlace] = {total: 0, candidates: {}, lists:{}};
                        $.each(app.candidates, function (candidate, config) {
                            app.votes.pollingPlaces[pollingPlace].candidates[slugify(candidate)] = 0;
                            app.votes.pollingPlacesTables[pollingPlace] = {};
                        });

                        $.each(pollingPlaceVotes, function(pollingPlaceTable, pollingPlaceTableVotes) {
                            app.votes.pollingPlacesTables[pollingPlace][pollingPlaceTable] = {total: 0, candidates: {}, lists: {}};
                            $.each(app.candidates, function (candidate, config) {
                                app.votes.pollingPlacesTables[pollingPlace][pollingPlaceTable].candidates[slugify(candidate)] = 0;
                            });

                            $.each(pollingPlaceTableVotes.candidates, function(candidate, votes) {
                                if (candidate === "Total") {
                                    app.votes.total += votes;
                                    app.votes.pollingPlaces[pollingPlace].total += votes;
                                    app.votes.pollingPlacesTables[pollingPlace][pollingPlaceTable].total += votes;
                                } else {
                                    app.votes.candidates[slugify(candidate)] += votes;
                                    app.votes.pollingPlaces[pollingPlace].candidates[slugify(candidate)] += votes;
                                    app.votes.pollingPlacesTables[pollingPlace][pollingPlaceTable].candidates[slugify(candidate)] += votes;
                                }
                            });

                            $.each(pollingPlaceTableVotes.lists, function(list, votes) {
                                if(typeof(app.votes.lists[slugify(list)]) === "undefined")
                                    app.votes.lists[slugify(list)] = 0;

                                app.votes.lists[slugify(list)] += votes;
                                app.votes.pollingPlaces[pollingPlace].lists[slugify(list)] += votes;
                                app.votes.pollingPlacesTables[pollingPlace][pollingPlaceTable].lists[slugify(list)] += votes;
                            })
                        })
                    });
                });

                let minibarConfig = {
                    barType: "default",
                    minBarSize: 10,
                    hideBars: false,  /* v0.4.0 and above */
                    alwaysShowBars: false,
                    horizontalMouseScroll: false,

                    scrollX: false,
                    scrollY: true,
                }

                // total votes
                $('#total-votes').html(
                    $('#tpl-total-votes')
                        .html()
                        .replace(/\{votes\}/g, app.votes.total)
                )

                // Candidate totals
                let currentCandidateScroll = $('#candidate-totals > .mb-content').scrollTop(),
                    votesSortedCandidates = [],
                    html = ''
                ;

                $.each(app.candidates, function(candidate, config) {
                    votesSortedCandidates.push([
                        candidate, slugify(candidate),
                        config, app.votes.candidates[slugify(candidate)]
                    ]);
                })
                votesSortedCandidates.sort((a,b) => b[3] - a[3])

                $.each(votesSortedCandidates, function(idx, data) {
                    let candidate = data[0],
                        slug = data[1],
                        config = data[2],
                        totalVotes = data[3],
                        totalPercent = app.votes.total ? ((totalVotes / app.votes.total) * 100).toFixed(1) : 0
                    ;

                    html += $('#tpl-item-total-votes')
                        .html()
                        .replace('{name}', candidate)
                        .replace(/\{slug\}/g, slug)
                        .replace('{votes}', totalVotes)
                        .replace(/\{percent\}/g, totalPercent)
                        .replace('{color}', config.color)
                        .replace('{image}', config.image)
                });

                let $htmlCandidates = $('<div>').append($(html))

                new MiniBar(
                    $htmlCandidates[0],
                    $.extend({}, minibarConfig, {
                        "onInit": function() {
                            $('#candidate-totals')
                                .addClass('mb-container')
                                .empty()
                                .append($htmlCandidates.children())
                                .find('.mb-content')
                                   .scrollTop(currentCandidateScroll)
                            ;
                        }
                    })
                );

                // Lists totals
                let currentListScroll = $('#list-totals').scrollTop();
                let votesSortedLists = [];
                html = '';

                $.each(app.lists, function(list, config) {
                    votesSortedLists.push([
                        list, slugify(list),
                        config, app.votes.lists[slugify(list)]
                    ]);
                })
                votesSortedLists.sort((a,b) => b[3] - a[3])

                $.each(votesSortedLists, function(idx, data) {
                    let list = data[0],
                        slug = data[1],
                        config = data[2],
                        totalVotes = data[3],
                        totalPercent = app.votes.total ? ((totalVotes / app.votes.total) * 100).toFixed(1) : 0
                    ;
                        html += $('#tpl-item-total-votes')
                            .html()
                            .replace('{name}', list)
                            .replace(/\{slug\}/g, slug)
                            .replace('{votes}', totalVotes)
                            .replace(/\{percent\}/g, totalPercent)
                            .replace('{color}', config.color)
                            .replace('{image}', config.image)
                    ;
                })

               let $htmlList = $('<div>').append($(html))

                new MiniBar(
                    $htmlList[0],
                    $.extend({}, minibarConfig, {
                        "onInit": function() {
                            $('#list-totals')
                                .addClass('mb-container')
                                .empty()
                                .append($htmlList.children())
                                .find('.mb-content')
                                   .scrollTop(currentListScroll)
                            ;
                        }
                    })
                );

                /*
                var votes = app.votes.pollingPlaces,
                    $pollingPlacesVotes = $('#polling-places-votes'),
                    templateHTML = $('#tpl-polling-place-votes').html(),
                    html = ''
                ;

                for(var pollingPlace in app.votes.pollingPlaces) {
                    var pollingPlaceVotes = app.votes.pollingPlaces[pollingPlace];
                    var bar = '<table cellpadding="0" cellspacing="0" class="w-100 border percent"><tr>';

                    for(var candidate in app.candidates) {
                        var percent = 0;

                        if(pollingPlaceVotes.total)
                            percent = ((pollingPlaceVotes[slugify(candidate)] / pollingPlaceVotes.total) * 100).toFixed(1);

                        if((percent % 1) === 0)
                            percent = parseFloat(percent).toFixed(0);

                        bar += (
                            '<td class="text-center border overflow-hidden percent" '
                            + ' title="' + pollingPlaceVotes[slugify(candidate)] + ' votos - ' + percent + '%" '
                            + 'style="width: ' + percent + '%;'
                            + 'background-color: ' + app.candidates[candidate].color + ';'
                            + 'cursor: default;'
                            + 'font-size: 75%">' + pollingPlaceVotes[slugify(candidate)] +'</td>'
                        );
                    }
                    bar += '<td style="width: 100%" class="percent"></td></tr></table>';

                    html += templateHTML
                        .replace('{bar}', bar)
                        .replace('{total-votes}', pollingPlaceVotes.total)
                        .replace('{name}', pollingPlace)
                    ;
                }

                $pollingPlacesVotes.empty().html(html);
                */
                setTimeout(() => app.loadDashboardVotes(), 3000)
            }
        );
    },
    setLocationTitle: function(comuna, pollingPlace, table) {
        $('#title')
            .empty()
            .append(
                '<span class="orange">' + comuna + '</span>' +
                ' 🢒 <span class="orange">' + pollingPlace + '</span>' +
                ' 🢒 <span class="orange">' + table + '</span>'
            )
    },
    setPollingPlaceTable: function(comunaID, pollingPlaceID, pollingPlaceTableID) {
        let $votes = $("#votes"),
            go = app.recover || app.current.clearVotesInChange(true)
        ;

        if(!go)
            return;

        $votes.empty();

        app.current.comuna = comunaID;
        app.current.pollingPlace = pollingPlaceID;
        app.current.pollingPlaceTable = pollingPlaceTableID;


        $votes.append(
            $(
                $('#template-candidates')
                    .html()
                    .replace('{name}', 'Total')
                    .replace(/\{slug\}/g, 'total')
                    .replace('{image}', 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')
                    .replace('{id}', '')
            )
                .removeClass('mb-3').addClass('mb-5')
                .find('div.orange').removeClass('orange').end()
                .find('img.border-orange').removeClass('border-orange').end()
        )

        $.each(app.candidates, function (candidate, config) {
            let slug = slugify(candidate),
                html = $('#template-candidates')
                    .html()
                    .replace('{name}', candidate)
                    .replace(/\{slug\}/g, slug)
                    .replace('{image}', config.image)
                    .replace('{id}', config.id)
            ;

            $votes.append($(html));
        })

        app.loadPollingPlaceTableVotes(comunaID, pollingPlaceID, pollingPlaceTableID)
    },
    _votesCallback: function(votes) {
        for(let v in votes) {
            let vote = votes[v];

            $('#candidate-' + slugify(vote.name || 'total') + '-votes input')
                .val(vote.count)
                .data({'value': vote.count})
                .trigger('input')
            ;
        }

        if(this.recover) {
            for(let inputID in this.recover.votes) {
                $('#' + inputID)
                    .val(this.recover.votes[inputID])
                    .trigger('input')
            }

            this.recover = null;
        }
    },
    loadPollingPlaceTableVotes: function(comunaID, pollingPlaceID, pollingPlaceTableID, block) {
        if(block !== false)
            app.block();

        $.getJSON(
            '/api/comunas/' + comunaID + '/polling-places/' + pollingPlaceID + '/tables/' + pollingPlaceTableID + '/votes/',
            function (votes) {
                app._votesCallback(votes);
                app.unblock();
            }
        )
            .fail(app.unblock)
        ;
    },
    loadSideMenu: function() {
        $.getJSON(
            '/api/comunas', function (comunas) {
                $('#comunas').empty();
                app.checkPendingVotes();

                for (var i in comunas) {
                    var $entryComuna = $('<li><a>' + comunas[i].name + '</a></li>'),
                        $submenuComuna = $('<ul/>')
                    ;

                    $('#comunas').append($entryComuna);
                    $entryComuna
                        .children('ul').empty().remove().end()
                        .append($submenuComuna)
                        .children('a')
                        .attr('id', 'comuna-' + comunas[i].id)
                        .data('comuna-id', comunas[i].id)
                        .on('click', function (evt) {
                            var self = this,
                                $submenuComuna = $(this).siblings('ul').empty()
                            ;

                            evt.stopImmediatePropagation();
                            evt.preventDefault();

                            app.block();

                            $.getJSON(
                                '/api/comunas/' + $(this).data('comuna-id') + '/polling-places/',
                                function (pollingPlaces) {
                                    for (var k in pollingPlaces) {
                                        var $entryPollingPlace = $('<li><a>' + pollingPlaces[k].name + '</a></li>');

                                        $submenuComuna.append($entryPollingPlace);
                                        $entryPollingPlace
                                            .siblings('ul').empty().remove().end()
                                            .append('<ul/>')
                                            .children('a')
                                            .attr(
                                                'id',
                                                'polling-place-'
                                                + $(self).data('comuna-id') + '-'
                                                + pollingPlaces[k].id
                                            )
                                            .data('comuna-id', $(self).data('comuna-id'))
                                            .data('polling-place-id', pollingPlaces[k].id)
                                            .on('click', function () {
                                                var self = this,
                                                    $submenuPollingPlace = $(this).siblings('ul').empty()
                                                ;

                                                evt.stopImmediatePropagation();
                                                evt.preventDefault();

                                                app.block();

                                                $.getJSON(
                                                    '/api/comunas/' + $(self).data('comuna-id') + '/polling-places/' + $(self).data('polling-place-id') + '/tables/',
                                                    function (pollingPlaceTables) {
                                                        for (var j in pollingPlaceTables) {
                                                            var $entryPollingPlaceTable = $('<li><a>' + pollingPlaceTables[j].name + '</a></li>');
                                                            $submenuPollingPlace.append($entryPollingPlaceTable);
                                                            $entryPollingPlaceTable
                                                                .children('a')
                                                                .attr(
                                                                    'id',
                                                                    'table-'
                                                                    + $(self).data('comuna-id')
                                                                    + '-' + $(self).data('polling-place-id')
                                                                    + '-' + pollingPlaceTables[j].id
                                                                )
                                                                .data('comuna-id', $(self).data('comuna-id'))
                                                                .data('polling-place-id', $(self).data('polling-place-id'))
                                                                .data('polling-place-table-id', pollingPlaceTables[j].id)
                                                                .on('click', function (evt) {
                                                                    var $this = $(this),
                                                                        $pollingPlaceAnchor = $this.parent().parent().siblings('a'),
                                                                        $comunaAnchor = $pollingPlaceAnchor.parent().parent().siblings('a')
                                                                    ;

                                                                    evt.stopImmediatePropagation();
                                                                    evt.preventDefault();

                                                                    app.setPollingPlaceTable(
                                                                        $this.data('comuna-id'),
                                                                        $this.data('polling-place-id'),
                                                                        $this.data('polling-place-table-id'),
                                                                    );

                                                                    app.setLocationTitle(
                                                                        $pollingPlaceAnchor.text(),
                                                                        $comunaAnchor.text(),
                                                                        $this.text()
                                                                    );
                                                                })
                                                        }

                                                        if(app.recover)
                                                            $(
                                                                '#table-' + app.recover.location.comuna
                                                                + '-' + app.recover.location.pollingPlace
                                                                + '-' + app.recover.location.pollingPlaceTable
                                                            ).trigger('click');

                                                        app.unblock();
                                                        // $('ul > li > ul > li > ul > li > a').eq(0).trigger('click');
                                                    }
                                                )
                                                    .fail(app.unblock)
                                                ;
                                            });
                                    }

                                    if(app.recover)
                                        $(
                                            '#polling-place-' + app.recover.location.comuna
                                            + '-' + app.recover.location.pollingPlace
                                        ).trigger('click');
                                    // $('ul > li > ul > li > a').eq(0).trigger('click');

                                    app.unblock();
                                }
                            )
                                .fail(app.unblock)
                            ;
                        });
                }

                if(app.recover)
                    $('#comuna-' + app.recover.location.comuna).trigger('click')

                app.unblock();
            }
        )
            .fail(app.unblock)
        ;
    },
    block: function() {
        $('#block').show();
    },
    unblock: function() {
        $('#block').hide();
    }
};