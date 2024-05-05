import { MdGamepad } from "react-icons/md";

const Logo = () => {
  return (
    <>
      <h1 className="text-black select-none text-4xl md:text-7xl lg:text-8xl bg-clip-text text-center tracking-widest">
        TrashGame
        <MdGamepad className="text-black inline-flex" />
      </h1>
    </>
  );
};

export default Logo;
