(() => {
    const langTools = ace.require("ace/ext/language_tools");
    const editor = ace.edit("editor");

    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/python");
    editor.setShowInvisibles(true);
    editor.setDisplayIndentGuides(true);
    editor.getSession().setUseWrapMode(true);
    editor.setOptions({
        enableBasicAutocompletion: true,
        enableLiveAutocompletion: true
    });

    const quantCompleter = {
        getCompletions: (editor, session, pos, prefix, callback) => {
            if (prefix.length === 0) {
                callback(null, []);
                return;
            }

            const charBeforePrefix = session.doc.$lines[pos.row][pos.column - 1 - prefix.length];

            if (/"|'/.test(charBeforePrefix)) {
                $.post('/editor/stock_complete', { prefix: prefix }, wordList => {
                    const completions = wordList.map(ea => ({
                        value: ea.value,
                        meta: ea.meta
                    }));
                    callback(null, completions);
                }, 'json');

                return;
            }

            $.post('/editor/code_complete', {
                source: session.getValue(),
                row: pos.row + 1,
                column: pos.column
            }, wordList => {
                const completions = wordList.map(ea => ({
                    value: ea.value,
                    meta: "cloud"
                }));
                callback(null, completions);
            }, 'json');
        }
    };

    langTools.addCompleter(quantCompleter);
})();