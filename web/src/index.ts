import {show_unread_recap} from "./recap";
console.log("INDEX TS LOADED");
(window as any).show_unread_recap = show_unread_recap;
import "./recap";
export { show_unread_recap } from "./recap";

// Ensure topic improver runs when included in bundle (client code must call its function where messages are sent)
import "./topic_improver";