const GameCard = ({
  game: {
    name,
  },
}) => {
  return (
    <div className="bg-black/70 m-5 p-0 rounded-xl shadow-lg shadow-black border-solid border-4 border-black max-w-[640px] hover:scale-105 ease-in duration-300">
      <h1 className="text-center text-4xl text-gray-200 tracking-wide font-bold mt-2 font-mono">
        {name}
      </h1>
    </div>
  );
};

export default GameCard;
