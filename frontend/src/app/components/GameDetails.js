import React, { useState, useEffect, useRef } from "react";

const GameDetails = ({ game, goBack }) => {
  const [analyze, setAnalyze] = useState("");
  const [loading, setLoading] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isFetched, setIsFetched] = useState(false);
  const analyzeRef = useRef("");

  useEffect(() => {
    console.log(analyzeRef.current)
    const fetchAdvantagesAndDisadvantages = async () => {
      setLoading(true);
      try {
        if (!isFetched) {
          setIsFetched(true);
          const response = await fetch(`https://trashgame-back.onrender.com/analyze/${game.id}/${game.name}`);
          const data = await response.json();
          analyzeRef.current = data.response;
          //setAnalyze(data.response);
        }
      } catch (error) {
        console.error("Error fetching advantages and disadvantages:", error);
      }
      setLoading(false);
      setIsLoading(false);
    };

    fetchAdvantagesAndDisadvantages();
  }, []);

  const renderAnalyze = () => {
    if (isLoading){
      return <p className="text-gray-200 text-center">Cargando análisis...</p>;
    }
    else if (!analyzeRef.current) {
      return <p className="text-gray-200 text-center">No se encontraron reseñas</p>;
    }

    const sections = analyzeRef.current.split("**");
    return (
      <div className="text-gray-200 text-center">
        {sections.map((section, index) => (
          <div key={index} className="mt-4">
            {index % 2 === 0 ? (
              <h2 className="list-disc list-inside">{section}</h2>
            ) : (
              <ul className="text-2xl font-semibold">
                {section
                  .split("*")
                  .filter(item => item.trim())
                  .map((item, i) => (
                    <li key={i}>{item.trim()}</li>
                  ))}
              </ul>
            )}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="flex justify-center items-center h-screen">
        <div className="bg-black/70 m-5 p-6 rounded-xl shadow-lg shadow-black border-solid border-4 border-black max-w-[640px] hover:scale-105 ease-in duration-300 max-h-[90%] overflow-auto">
        <button onClick={goBack} className="text-gray-200 hover:text-white hover:underline">Go Back</button>
        <h1 className="text-center text-4xl text-gray-200 tracking-wide font-bold mt-2 font-mono">{game.name}</h1>
        <h2 className="text-center text-2xl text-gray-200 tracking-wide font-semibold mt-4">Análisis</h2>
        {loading ? (
            <p className="text-gray-200 text-center">Cargando análisis...</p>
        ) : (
          renderAnalyze()
        )}
        </div>
    </div>
  );
};

export default GameDetails;
