API_KEY = "62e6c984f9f3b22cc8c25e2136431d02"
API_ATOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2MmU2Yzk4NGY5ZjNiMjJjYzhjMjVlMjEzNjQzMWQwMiIsInN1YiI6IjY2MjA0ZmUwM2Y0ODMzMDE4NjczMGQ0NSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.kWMQDX-qrAB8sZtSpP2L5Q05ZF_ZvFzQNhUkG6YxGgg"

// Using the Tmbd database
// after fetch request, is updated with
// the genres available
//  these are parallel arrays, so each one corresponds
// with the other
var genres = []
var genre_ids = []
// Generate Genre Options
const options = {
    method: 'GET',
    headers: {
      accept: 'application/json',
      Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2MmU2Yzk4NGY5ZjNiMjJjYzhjMjVlMjEzNjQzMWQwMiIsInN1YiI6IjY2MjA0ZmUwM2Y0ODMzMDE4NjczMGQ0NSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.kWMQDX-qrAB8sZtSpP2L5Q05ZF_ZvFzQNhUkG6YxGgg'
    }
  };
fetch('https://api.themoviedb.org/3/genre/movie/list?language=en', options)
    .then(response => response.json())
    .then(response => {
        genres = response["genres"].map(genre => genre.name)
        genre_ids = response["genres"].map(genre => genre.id)
        $("#genres").append(response["genres"].map(genre_dict => {
            return (
                `
                <input 
                    id="genre-${genre_dict.name}" 
                    type="checkbox" 
                    name="genre-${genre_dict.name}" 
                    value="${genre_dict.name}"/>
                <label for="genre-comedy">${genre_dict.name}</label>
                `
            )
        }))
        genres.push("any")
    })
    .catch(err => console.error(err));

function getImportance(name){
    /*
     * Returns the importance level that the
     * user has selected. Assumes that the radio
     * inputs follow the id naming convention
     * [name]-important, [name]-simportant, and
     * [name]-nimportant AND that radio buttons
     * have a value attribute defined
     */
    var ids = [`#${name}-important`, `#${name}-simportant`, `#${name}-nimportant`]
    var selection = "None Selected"
    ids.forEach(id => {
        // if the id has been checked, then return
        // that importance value
        if($(id).is(":checked")){
            selection = $(id).val();
        }
    })
    return selection
}  

function getSelectedGenres(){
    /**
     * Returns an array of the 
     * genres that the user has 
     * selected (from its value)
     * as their ids
     * If any genre is checked,
     * then returns empty array
     */
    if($("#genre-any").is(":checked")){ // return all genres
        return []
    }
    else{
        var output = []
        for(let i = 0; i < genres.length; i++){
            genre = genres[i]
            if($(`#genre-${genre}`).is(":checked")){
                output.push(genre_ids[i])
            }
        }
        return output
    }

}
function getImagePath(path){
    // Returns the image address given a particular path
    return "https://image.tmdb.org/t/p/original" + path
}

function getFieldsetChoice(id){
    // given the id of a fieldset (i.e language-fieldset)
    // will return the value of the checked radio button
    return $('input:checked', '#'+id).val()
}

// // test a function by calling alert on it
// $(document).on('keypress', function(e) {
//     if(e.keyCode = 32){ // if spacebar
//         alert(getFieldsetChoice("language-field"))
//     }
// });

$("#rec-button").click(() => {
    // DEBUGGING
    console.log(genres)
    console.log(getImportance("genre"))
    var selected_genres = getSelectedGenres()
    console.log(selected_genres)
    console.log(genre_ids)
    // Fetch movies that match genre requirements
    // Uses the decision based system
    // to generate the query URL
    var url = "https://api.themoviedb.org/3/discover/movie?page=1"
    if(selected_genres.length > 0){ // only add genre param IF user has specified
        var param = "&with_genres="
        // the comma (,) acts as an AND operator for the API
        param += selected_genres.join(",")
        console.log(param)
        url += param
    }
    languageVal = getFieldsetChoice("language-field")
    if(languageVal){
        // Append language parameter to the URL
        var langParam = "&language=" + languageVal;
        console.log(langParam)
        url += langParam;
    }

    // Get selected sort option
    var sortBy = $("#sort-by").val();
    if (sortBy) {
        url += "&sort_by=" + sortBy;
    }

    // basic no need to change
    const options = {
        method: 'GET',
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2MmU2Yzk4NGY5ZjNiMjJjYzhjMjVlMjEzNjQzMWQwMiIsInN1YiI6IjY2MjA0ZmUwM2Y0ODMzMDE4NjczMGQ0NSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.kWMQDX-qrAB8sZtSpP2L5Q05ZF_ZvFzQNhUkG6YxGgg'
        }
      };
      
      // fetch data from API and show on page
      fetch(url, options)
        .then(response => response.json())
        .then(response => {
            results = response["results"]
            console.log(response)
            $("#results").empty()
            results.forEach(movie => {
                $("#results").append(
                    `
                    <div class="movie-container">
                        <div class="movie-info">
                            <h3>${movie.title}</h3>
                            <p>${movie.overview}</p> <!-- Display movie synopsis -->
                        </div>
                        <img class="movie-poster" src="${getImagePath(movie.poster_path)}"/>
                    </div>
                    `
                )
            })
            // append explanation, modify the explanation
            // build one based on the quiz responses
            $("#res-desc").empty()
            $("#res-desc").append("This is the explanation")
        })
        .catch(err => console.error(err));

})
