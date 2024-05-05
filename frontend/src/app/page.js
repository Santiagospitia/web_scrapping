'use client'
import { useState, useEffect } from "react";
import { FaSearch } from "react-icons/fa";
import { Oval } from "react-loading-icons";
import "./App.css";
import GameCard from "./components/GameCard";
import Nav from "./components/Nav";
import Logo from "./components/Logo";
import GameDetails from "./components/GameDetails";

let numResults;

const App = () => {
  console.log('Rendering App');
  const [searchTerm, setSearchTerm] = useState("");
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedGame, setSelectedGame] = useState(null);
  let [counter, setCounter] = useState(1);

  const increment = () => {
    setCounter(counter += 1);
    searchGames(searchTerm);
  };

  const decrement = () => {
    if (counter >= 2) {
      setCounter(counter -= 1);
      searchGames(searchTerm);
    }
  };

  const searchGames = async (title) => {
    setLoading(true);
    if (title !== "") {
      const response = await fetch(
        `http://localhost:5000/search/${title}`
      );
      const data = await response.json();
      console.log("holis", data)
      setGames(data);
      numResults = data.length;
    }
    setLoading(false);
  };

  const handleGameClick = (game) => {
    setSelectedGame(game);
  };

  const goBack = () => {
    setSelectedGame(null);
  };

  if (selectedGame) {
    return (
      <GameDetails game={selectedGame} goBack={goBack} />
    );
  }

  return (
    <>
      <div className="w-full h-full p-2">
        <Logo />
        <div className="flex justify-center mt-2">
          <input
            className="text-3xl rounded-xl p-3 shadow-md shadow-black text-gray-200 bg-black/70 border-2 border-black w-[70%] max-w-[800px] capitalize"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search Games . . ."
            onKeyPress={(e) => {
              if (e.key === "Enter") {
                setCounter(counter = 1);
                searchGames(searchTerm);
              }
            }}
            type="text"
          />{" "}
          <button
            onClick={() => {
              searchGames(searchTerm);
            }}
            className="ml-3 bg-black/70 border-2 border-black p-3 rounded-2xl text-gray-200 md:shadow-md md:shadow-black hover:bg-black/90 hover:scale-110 ease-in duration-300"
          >
            {!loading ? <FaSearch size={35} /> : <Oval />}
          </button>
        </div>
        <div className="flex justify-center">
          {games.length > 0 ? (
            <div>
              <Nav
                counter={counter}
                decrement={() => decrement()}
                increment={() => increment()}
              />
              {/* grid of games */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-2 ">
                {games.map((item, index) => (
                  <div key={index} onClick={() => handleGameClick(item)}>
                    <GameCard game={item} />
                  </div>
                ))}
              </div>
              <Nav
                counter={counter}
                decrement={() => decrement()}
                increment={() => increment()}
              />
            </div>
          ) : (
            <>
              {numResults === undefined ? null : (
                <p className="text-center mt-5 text-xl text-gray-200 border-2 border-black bg-black/70 py-2 px-4 rounded-xl">
                  No games found . . .
                </p>
              )}
            </>
          )}
        </div>
      </div>
    </>
  );
};

export default App;
