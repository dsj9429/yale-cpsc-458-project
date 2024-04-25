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
    var url = "https://api.themoviedb.org/3/discover/movie?language=en-US&page=1&sort_by=popularity.desc"
    if(selected_genres.length > 0){ // only add genre param IF user has specified
        var param = "&with_genres="
        // the comma (,) acts as an AND operator for the API
        param += selected_genres.join(",")
        console.log(param)
        url += param
    }
    console.log(url)
    const options = {
        method: 'GET',
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2MmU2Yzk4NGY5ZjNiMjJjYzhjMjVlMjEzNjQzMWQwMiIsInN1YiI6IjY2MjA0ZmUwM2Y0ODMzMDE4NjczMGQ0NSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.kWMQDX-qrAB8sZtSpP2L5Q05ZF_ZvFzQNhUkG6YxGgg'
        }
      };
      
      fetch(url, options)
        .then(response => response.json())
        .then(response => {
            results = response["results"]
            console.log(response)
            $("#results").empty()
            results.forEach(movie => {
                $("#results").append(
                    `
                    <div>
                        <h3>${movie.title}</h3>
                        <img width="200px" src="${getImagePath(movie.poster_path)}"/>
                    </div>
                    `
                )
            })
        })
        .catch(err => console.error(err));
})