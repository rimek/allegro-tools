/*jshint esversion: 6 */
'use strict';


const e = React.createElement;

class SearchForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        search: []
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
      let state = this.state;
      state.search[event.target.id] = event.target.value;
      this.setState(state);
  }

  handleSubmit(event) {
      // alert('search for: ' + Object.values(this.state.search));
      event.preventDefault();

      let payload = JSON.stringify(Object.values(this.state.search));

        fetch('/search', {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: 'post',
            body: payload
        })
          .then(res => res.json())
          .then(
              (result) => {
                  console.log(result);
              },
              (error) => {
                  console.log(error);
              });
  }

  render() {
        return (
            <form onSubmit={this.handleSubmit} className="form-inline">
                <div className="form-group col-4">
                    <label> Search phrase 1: </label>
                    <input type="text" id="search1" value={this.state.search1} onChange={this.handleChange} className="form-control" />
                </div>

                <div className="form-group col-4">
                    <label> Search phrase 2: </label>
                    <input type="text" id="search2" value={this.state.value} onChange={this.handleChange} className="form-control" />
                </div>

                <button type="submit" className="btn btn-primary">Submit</button>
            </form>
        );
    }
}


const domContainer = document.querySelector('#react-form');
ReactDOM.render(e(SearchForm), domContainer);
