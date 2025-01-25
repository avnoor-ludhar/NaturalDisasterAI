import { Button } from "./ui/button";
import {
    NavigationMenu,
    NavigationMenuContent,
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList,
    NavigationMenuTrigger,
    navigationMenuTriggerStyle
  } from "./ui/navigation-menu";

import { Link, NavigateFunction, useLocation } from "react-router-dom";
import { useAppSelector } from "@/redux/store";
import { User } from "@/redux/features/userSlice";
import { useLogout, LogoutHook } from "@/hooks/useLogout";
import { useNavigate } from "react-router-dom";

//navbar to move between pages
export default function Navbar(): JSX.Element{
    const user: User | null = useAppSelector<User | null>(state=>state.user.user);
    const {logout}: LogoutHook = useLogout();
    const navigate: NavigateFunction = useNavigate();
    const location = useLocation();

    function handleClick(e: React.SyntheticEvent<HTMLButtonElement>): void {
        e.preventDefault();
        logout();
        navigate('/');
    }

    //routes that will hide the navbar through conditional tests
    const showNavbarRoutes = ['/home', '/disaster-form', '/disaster-view'];
    const shouldShowNavbar = showNavbarRoutes.includes(location.pathname);

    return(
        <div>
            <nav className='w-full flex flex-row justify-between items-center px-10 py-6 font-Montserrat'>
                <Link to="/" className="flex flex-row items-center">
                    <p className="text-2xl font-bold leading-10 text-center bg-gradient-to-r from-red-500 via-red-700 to-black text-transparent bg-clip-text">
                        NaturalDisasterAI
                    </p>
                </Link>
                
                <div className="flex flex-row items-center">
                    <NavigationMenu className="flex">
                        {shouldShowNavbar && <NavigationMenuList>
                            <NavigationMenuItem >
                            <NavigationMenuTrigger className="bg-gray-100 text-lg w-full">Options</NavigationMenuTrigger>
                            <NavigationMenuContent>
                                <Link to="/home" >
                                    <NavigationMenuLink className={navigationMenuTriggerStyle()}>Home</NavigationMenuLink>
                                </Link>
                                <Link to="/disaster-form" >
                                    <NavigationMenuLink className={navigationMenuTriggerStyle()}>Add Updates</NavigationMenuLink>
                                </Link>
                                <Link to="/disaster-view" >
                                    <NavigationMenuLink className={navigationMenuTriggerStyle()}>View Recent Updates</NavigationMenuLink>
                                </Link>
                                <Link to="/prev-data" >
                                    <NavigationMenuLink className={navigationMenuTriggerStyle()}>Generate itinerary</NavigationMenuLink>
                                </Link>
                            </NavigationMenuContent>
                            </NavigationMenuItem>
                        </NavigationMenuList>}
                    </NavigationMenu>
                    { user ? (<Button onClick={handleClick} variant = "ghost" className="text-lg h-[40px] flex ">Log Out</Button>) : (<><Link to='/login'><Button variant = "ghost" className="text-lg h-[40px] hidden md:flex ">Log In</Button></Link><Link to="/signup"><Button variant = "outline" className="dark:text-white text-md mx-5 rounded-md h-[40px] hover:opacity-90 md:w-[84px] hidden md:flex">Sign up</Button></Link></>)}
                </div>
            </nav>
        </div>
    )
};
       