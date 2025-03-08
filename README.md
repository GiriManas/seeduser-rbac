TableHeader>
          <TableBody>
            {userList.map((user: PendingUser) => (
              <TableRow key={user.id} className="border-b hover:bg-gray-100">
                <TableCell className="px-4 py-2">{user.id}</TableCell>
                <TableCell className="px-4 py-2">{user.email}</TableCell>
                <TableCell className="px-4 py-2">{user.name}</TableCell>
                <TableCell className="px-4 py-2">{user.approver}</TableCell>
                <TableCell className={`px-4 py-2 font-medium ${user.status === "Approved" ? "text-green-600" : user.status === "Declined" ? "text-red-600" : "text-yellow-600"}`}>
                  {user.status}
                </TableCell>
                <TableCell className="px-4 py-2 flex gap-3">
                  {user.status === "Pending" && (
                    <>
                      <button onClick={() => handleApprove(user.id)} className="text-green-500 hover:text-green-700">
                        <CheckIcon className="h-5 w-5" />
                      </button>
                      <button onClick={() => handleDecline(user.id)} className="text-red-500 hover:text-red-700">
                        <XCircleIcon className="h-5 w-5" />
                      </button>
                    </>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>