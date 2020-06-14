var Search = {

    searchForm: $("#search-form"),
    searchTerms: $("#search-terms"),
    searchFilters: $("#search-filters"),
    searchFiltersTitle: $("#search-filters-title"),
    offset: $("#search-filters-title").offset(),
    win: $(window),

    init: function () {
        Search.bindUIEvents();
    },

    bindUIEvents: function () {

        Search.searchFiltersTitle
            .on(
                "click",
                Search.toggleSearchFilters
            );

        Search.win
            .on(
                "scroll",
                Search.filterHeaderPosition
            );

        Search.searchForm
            .on(
                "submit",
                Search.searchSubmit
            );

    },

    toggleSearchFilters: function () {
        Search.searchForm
            .toggleClass("filters-open");
    },

    filterHeaderPosition: function () {

        var scrollTop = Search.win.scrollTop();

        if (scrollTop > Search.offset.top) {
            Search.searchFilters.addClass("pinned");
            Search.searchTerms.css("margin-bottom", Search.searchFilters.outerHeight());
        } else {
            Search.searchFilters.removeClass("pinned");
            Search.searchTerms.css("margin-bottom", "10px");
        };

    },

    searchSubmit: function () {
        // process new search
        return false;
    }

};

Search.init();