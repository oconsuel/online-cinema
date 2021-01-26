$('#delete-movie-modal').on('show.bs.modal', function (event) {
    let url = event.relatedTarget.dataset.url;
    let form = this.querySelector('form');
    form.action = url;
    let movieName = event.relatedTarget.dataset.movie;
    this.querySelector('#movie-name').textContent = movieName;
})