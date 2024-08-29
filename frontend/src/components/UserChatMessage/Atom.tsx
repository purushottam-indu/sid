import { atom } from "recoil";
 
export const selectedMessageAtom = atom<string>({
    key: "selectedMessage",
    default: ""
});
 