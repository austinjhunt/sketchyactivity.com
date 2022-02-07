import React from "react";
import "./App.css";
import $ from "jquery";
import AOS from "aos";

const api = "http://localhost:8000/api";

function k() {
  return "52cdcc726dabfbe7356dc273f2f5a238f6d40c10";
}

function App() {
  return <Sketchbook></Sketchbook>;
}

class PortfolioPages extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      portfolio: [],
    };
  }
  componentDidMount() {
    fetch(`${api}/portfolio`, {
      method: "GET",
      headers: {
        Authorization: `Token ${k()}`,
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((json) => this.setState({ portfolio: json }));
  }
  render() {
    return this.state.portfolio.map((portfolio_item, index) => {
      return (
        <SketchbookPage
          key={index}
          portfolio_item={portfolio_item}
          index={index}
        ></SketchbookPage>
      );
    });
  }
}

class Sketchbook extends React.Component {
  render() {
    return (
      <HTMLFlipBook width={300} height={500}>
        <PortfolioPages></PortfolioPages>
      </HTMLFlipBook>
    );
  }
}

const SketchbookPage = React.forwardRef((props, ref) => {
  return props.portfolio_item ? (
    <div className="sketchbook-page" ref={ref}>
      <div
        className="col-xs-1 col-sm-1 col-md-3 col-lg-3  ftco-animate portfolioItem"
        data-aos="fade-down"
        key={props.portfolio_item.id}
      >
        <a
          data-id={props.portfolio_item.id}
          href={props.portfolio_item.s3_copied_smaller_drawing_private_url}
          className="portfolio-entry img image-popup d-flex justify-content-center align-items-center"
          style={{
            backgroundImage: `url(${props.portfolio_item.s3_copied_smaller_drawing_private_url})`,
          }}
        >
          <div className="overlay"></div>
          <div className="text text-center">
            <h3>{props.portfolio_item.portrait_name}</h3>
            <span className="tag">{props.portfolio_item.tag}</span>
            <br />
            <span className="tag">{props.portfolio_item.date}</span>
          </div>
        </a>
      </div>
      <p>Page number: {props.index + 1}</p>
    </div>
  ) : (
    <div className="sketchbook-page" ref={ref}></div>
  );
});

AOS.init({
  duration: 800,
  easing: "slide",
});

var fullHeight = function() {
  $(".js-fullheight").css("height", $(window).height());
  $(window).resize(function() {
    $(".js-fullheight").css("height", $(window).height());
  });
};
fullHeight();

export default App;
