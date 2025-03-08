"""

return (
    <div className="p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-xl font-semibold mb-4">Users Table</h2>

      {/* 🔍 Search Input */}
      <input
        type="text"
        placeholder="Search users..."
        className="w-full p-2 border rounded mb-4"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />

      <div className="overflow-x-auto border rounded-lg shadow-sm">
        <Table className="w-full border-collapse">
          <TableHeader className="bg-gray-100 text-gray-700">
            <TableRow>
              <TableHead className="px-4 py-2 cursor-pointer" onClick={() => handleSort("id")}>
                ID {sortColumn === "id" && (sortOrder === "asc" ? <ArrowUpIcon className="h-4 w-4 inline" /> : <ArrowDownIcon className="h-4 w-4 inline" />)}
              </TableHead>
              <TableHead className="px-4 py-2 cursor-pointer" onClick={() => handleSort("username")}>
                Username {sortColumn === "username" && (sortOrder === "asc" ? <ArrowUpIcon className="h-4 w-4 inline" /> : <ArrowDownIcon className="h-4 w-4 inline" />)}
              </TableHead>
              <TableHead className="px-4 py-2">Roles</TableHead>
              <TableHead className="px-4 py-2">Groups</TableHead>
              <TableHead className="px-4 py-2 cursor-pointer" onClick={() => handleSort("created")}>
                Created {sortColumn === "created" && (sortOrder === "asc" ? <ArrowUpIcon className="h-4 w-4 inline" /> : <ArrowDownIcon className="h-4 w-4 inline" />)}
              </TableHead>
              <TableHead className="px-4 py-2">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {sortedUsers.map((user: User) => (
              <TableRow key={user.id} className="border-b hover:bg-gray-100">
                <TableCell className="px-4 py-2">{user.id}</TableCell>
                <TableCell className="px-4 py-2">{user.username}</TableCell>

                {/* Roles */}
                <TableCell className="px-4 py-2">
                  <div className="flex flex-wrap gap-2">
                    {user.roles.map((role, index) => (
                      <Badge key={index} type="role">{role}</Badge>
                    ))}
                  </div>
                </TableCell>

                {/* Groups */}
                <TableCell className="px-4 py-2">
                  <div className="flex flex-wrap gap-2">
                    {user.groups.map((group, index) => (
                      <Badge key={index} type="group">{group}</Badge>
                    ))}
                  </div>
                </TableCell>

                <TableCell className="px-4 py-2">{user.created}</TableCell>

                {/* Actions */}
                <TableCell className="px-4 py-2 flex gap-3">
                  {/* View Button */}
                  <button className="text-blue-500 hover:text-blue-700">
                    <EyeIcon className="h-5 w-5" />
                  </button>

                  {/* Edit Button */}
                  <button className="text-yellow-500 hover:text-yellow-700">
                    <PencilIcon className="h-5 w-5" />
                  </button>

                  {/* Delete Button */}
                  <button className="text-red-500 hover:text-red-700">
                    <TrashIcon className="h-5 w-5" />
                  </button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}





"""