import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function RightMenu() {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null); // Create a reference for the dropdown

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const closeDropdown = () => {
    setIsOpen(false);
  };

  // Detect click outside dropdown to close it
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        closeDropdown();
      }
    }

    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen]);

  return (
    <div className="relative" ref={dropdownRef}>
      <Button variant="ghost" className="flex justify-between p-2" onClick={toggleDropdown}>
        <p className="w-28 truncate">Admin</p>
      </Button>

      {isOpen && (
        <div className="absolute z-10 mt-2 w-44 rounded-lg shadow-lg bg-white ring-1 ring-black ring-opacity-5">
          <ul role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
            <li>
              <Link href="/admin/pendingusers" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" onClick={closeDropdown}>
                Pending Users
              </Link>
            </li>
            <li>
              <Link href="/admin/users" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" onClick={closeDropdown}>
                Users
              </Link>
            </li>
            <li>
              <Link href="/admin/roles" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" onClick={closeDropdown}>
                Roles
              </Link>
            </li>
            <li>
              <Link href="/admin/groups" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" onClick={closeDropdown}>
                Groups
              </Link>
            </li>
          </ul>
        </div>
      )}
    </div>
  );
}