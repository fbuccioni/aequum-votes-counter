app.block();
    // $('#title').fitText(1.2);

    $('#votes').on('click', 'button', function() {
        let op = $(this).hasClass('add') ? 'add' : 'remove',
            cant = 1.
            id = $(this).parent().parent().data('id'),
            jsonOp = app.jsonOp(op, cant, (!id) ? null : id),
            $input = $(this).siblings('input'),
            $inputTotal = $('#candidate-total-votes input')
        ;

        $input.val(String(app.ops[op](parseInt($input.val()), cant)));
        app.opsQueue.push(jsonOp);

        if($inputTotal[0] != $input[0]) {
            $inputTotal.val(String(app.ops[op](parseInt($inputTotal.val()), cant)));
            app.opsQueue.push($.extend({}, jsonOp, {"candidate": null}));
        }
    });

    $('#votes')
        .on('click', 'button.cancel', function(evt) {
            let $input = $(this).siblings('input');
            $input
                .val($input.data('value'))
                .trigger('input')
            ;
        })
        .on('input', '.vote-input', function(evt) {
            let $this = $(this),
                isChanging = $this.val() !== $this.data('value').toString(),
                $cancelButton = $this.siblings('button').show()
            ;

            if(isChanging) {
                app.current.addVotesInChange(this.id, this.value);
                $('.save-changes').removeClass('d-none');
            } else {
                $cancelButton.hide();
                app.current.removeVotesInChange(this.id);

                if($.isEmptyObject(app.current.votesInChange))
                    $('.save-changes').addClass('d-none');
            }

            $cancelButton[isChanging ? 'removeClass' : 'addClass']('d-none');
        })

    $('.btn.cancel-all').on('click', function() {
       $('.vote-input').each(function() {
           let $cancelButton = $(this).siblings('button');
           if(!$cancelButton.hasClass('d-none')) {
               $cancelButton.trigger('click');
           }
       });
    });

    $('.btn.save-changes').on('click', function() {
        let op = 'set';

        $('.vote-input').each(function() {
            let id = $(this).parent().parent().data('id');
            if(!$(this).siblings('button.cancel').hasClass('d-none'))
                app.opsQueue.push(app.jsonOp(op, parseInt(this.value), (!id) ? null : id))
        });

        app.processQueue()
    })

    $('#content').on('click', function() {
        if($('.menu').css('transform') === 'none')
            $('.menu').addClass('close');
    });

    $('.btn-menu').on('click', function() {
        if($('.menu').css('transform') !== 'none')
            $('.menu').removeClass('close');
    });

    app.loadCandidates(function() {
        app.loadSideMenu();
    });
