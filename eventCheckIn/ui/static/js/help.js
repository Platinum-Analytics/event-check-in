$(".nav-link").each(
    function () {
        let tab = $(this)
        tab.on("hide.bs.tab", event => {
            $(event.target).toggleClass("fw-bold")
        })
        tab.on("show.bs.tab", event => {
            $(event.target).toggleClass("fw-bold")
        })
    }
)

