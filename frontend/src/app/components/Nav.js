import { FaArrowAltCircleRight, FaArrowCircleLeft } from "react-icons/fa";

const Nav = ({
  counter,
  decrement,
  increment,
}) => {
  return (
    <>
      <div className="flex justify-center">
        <div className="mt-2 text-xl font-mono min-w-[50%]">
          <div className="font-bold bg-black/70 border-2 border-black py-2 rounded-xl justify-between mt-2 flex text-gray-300 shadow-md shadow-black">
            <button
              className={
                "px-4 rounded-2xl hover:scale-110 transition-all duration-300 ease-in-out"
              }
              onClick={() => decrement()}
            >
              <FaArrowCircleLeft size={30} />
            </button>
            <span className="my-auto text-xl tracking-wide">
              Page {counter}
            </span>
            <button
              className={
                "px-4 rounded-2xl hover:scale-110 transition-all duration-300 ease-in-out"
              }
              onClick={() => increment()}
            >
              <FaArrowAltCircleRight size={30} />
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default Nav;
