<div className="p-6 bg-white shadow-lg rounded-lg max-w-7xl mx-auto w-full">
  <h2 className="text-2xl font-semibold mb-4 text-center">Pending Users</h2>

  {/* 🔍 Search & Filters */}
  <div className="flex flex-col sm:flex-row justify-between items-center mb-4 gap-4">
    <input
      type="text"
      placeholder="Search users..."
      className="p-2 border rounded w-full sm:w-1/3"
    />
    <select
      value={statusFilter}
      onChange={(e) => setStatusFilter(e.target.value)}
      className="p-2 border rounded w-full sm:w-auto"
    >
      <option value="All">All</option>
      <option value="Pending">Pending</option>
      <option value="Approved">Approved</option>
      <option value="Declined">Declined</option>
    </select>
  </div>

  {/* 📄 Table with Responsive Scroll */}
  <div className="overflow-x-auto border rounded-lg shadow-sm w-full">
    <Table className="w-full text-sm border-collapse">
      <TableHeader className="bg-gray-100 text-gray-700">
        <TableRow>
          <TableHead className="px-6 py-3">User ID</TableHead>
          <TableHead className="px-6 py-3">Email</TableHead>
          <TableHead className="px-6 py-3">Name</TableHead>
          <TableHead className="px-6 py-3">Approver</TableHead>
          <TableHead className="px-6 py-3">Status</TableHead>
          <TableHead className="px-6 py-3">Approval</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {paginatedUsers.map((user: PendingUser) => (
          <TableRow key={user.id} className="border-b hover:bg-gray-100">
            <TableCell className="px-6 py-3">{user.id}</TableCell>
            <TableCell className="px-6 py-3">{user.email}</TableCell>
            <TableCell className="px-6 py-3">{user.name}</TableCell>
            <TableCell className="px-6 py-3">{user.approver}</TableCell>
            <TableCell className="px-6 py-3">{user.status}</TableCell>
            <TableCell className="px-6 py-3 flex gap-3">
              {user.status === "Pending" && (
                <>
                  <button className="text-green-500 hover:text-green-700">
                    ✅ Approve
                  </button>
                  <button className="text-red-500 hover:text-red-700">
                    ❌ Decline
                  </button>
                </>
              )}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </div>
</div>