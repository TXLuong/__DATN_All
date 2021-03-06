/*!

=========================================================
* Material Dashboard React - v1.9.0
=========================================================

* Product Page: https://www.creative-tim.com/product/material-dashboard-react
* Copyright 2020 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/material-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
// @material-ui/icons
import Dashboard from "@material-ui/icons/Dashboard";
import Person from "@material-ui/icons/Person";
import LibraryBooks from "@material-ui/icons/LibraryBooks";
import BubbleChart from "@material-ui/icons/BubbleChart";
import LocationOn from "@material-ui/icons/LocationOn";
import Notifications from "@material-ui/icons/Notifications";
import Unarchive from "@material-ui/icons/Unarchive";
import Language from "@material-ui/icons/Language";
import AccessTimeIcon from '@material-ui/icons/AccessTime';
import PersonAddIcon from '@material-ui/icons/PersonAdd';
import RestorePageIcon from '@material-ui/icons/RestorePage';
// core components/views for Admin layout
import DashboardPage from "views/Dashboard/Dashboard.js";
import UserProfile from "views/UserProfile/UserProfile.js";
import TableList from "views/TableList/TableList.js";
import Typography from "views/Typography/Typography.js";
import Icons from "views/Icons/Icons.js";
import Maps from "views/Maps/Maps.js";
import NotificationsPage from "views/Notifications/Notifications.js";
import UpgradeToPro from "views/UpgradeToPro/UpgradeToPro.js";
// core components/views for RTL layout
import RTLPage from "views/RTLPage/RTLPage.js";
import TrackingTime from './views/TimeTracking/Tracking';
import WorkLog from "./views/workHistory/workLog";
import AddEmployee from './views/AddEmployee/AddEmployee';
const employeeRoutes = [
  {
    path: "/Tracking",
    name: "Tracking time",
    icon: AccessTimeIcon,
    component: TrackingTime,
    layout: "/employee"
  },
  {
    path : "/history",
    name : "Work history",
    icon : RestorePageIcon,
    component : WorkLog,
    layout : "/employee"
  },
  {
    path: "/employee",
    name: "User Profile",
    rtlName: "?????? ???????????? ????????????????",
    icon: Person,
    component: UserProfile,
    layout: "/employee"
  },
]
const dashboardRoutes = [
  {
    path: "/dashboard",
    name: "Dashboard",
    rtlName: "???????? ??????????????",
    icon: Dashboard,
    component: DashboardPage,
    layout: "/admin"
  },
  // {
  //   path: "/table",
  //   name: "Table List",
  //   rtlName: "?????????? ????????????",
  //   icon: "content_paste",
  //   component: TableList,
  //   layout: "/admin"
  // },
  {
    path: "/user",
    name: "User Profile",
    rtlName: "?????? ???????????? ????????????????",
    icon: Person,
    component: UserProfile,
    layout: "/admin"
  },
  // {
  //   path: "/Tracking",
  //   name: "Tracking time",
  //   icon: AccessTimeIcon,
  //   component: TrackingTime,
  //   layout: "/admin"
  // },
  // {
  //   path : "/history",
  //   name : "Work history",
  //   icon : RestorePageIcon,
  //   component : WorkLog,
  //   layout : "/admin"
  // },
  {
    path : "/addEmployee",
    name : "Add Employee",
    icon : PersonAddIcon,
    component : AddEmployee,
    layout : "/admin"
  }
  

  // {
  //   path: "/typography",
  //   name: "Typography",
  //   rtlName: "??????????",
  //   icon: LibraryBooks,
  //   component: Typography,
  //   layout: "/admin"
  // },
  // {
  //   path: "/icons",
  //   name: "Icons",
  //   rtlName: "????????????",
  //   icon: BubbleChart,
  //   component: Icons,
  //   layout: "/admin"
  // },
  // {
  //   path: "/maps",
  //   name: "Maps",
  //   rtlName: "??????????",
  //   icon: LocationOn,
  //   component: Maps,
  //   layout: "/admin"
  // },
  // {
  //   path: "/notifications",
  //   name: "Notifications",
  //   rtlName: "??????????????",
  //   icon: Notifications,
  //   component: NotificationsPage,
  //   layout: "/admin"
  // },
  // {
  //   path: "/rtl-page",
  //   name: "RTL Support",
  //   rtlName: "???????????????? ???? ???????? ???? ????",
  //   icon: Language,
  //   component: RTLPage,
  //   layout: "/rtl"
  // },
  // {
  //   path: "/upgrade-to-pro",
  //   name: "Upgrade To PRO",
  //   rtlName: "???????????? ????????????????????",
  //   icon: Unarchive,
  //   component: UpgradeToPro,
  //   layout: "/admin"
  // }
];

export default dashboardRoutes;
export {employeeRoutes};