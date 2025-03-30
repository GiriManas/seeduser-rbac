import { useState } from "react";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";

interface AddRoleModalProps {
  isOpen: boolean;
  onClose: () => void;
  accessToken: string; // Pass this from session
}

const AddRoleModal: React.FC<AddRoleModalProps> = ({ isOpen, onClose, accessToken }) => {
  const { register, handleSubmit, formState: { errors }, reset } = useForm();
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const onSubmit = async (data: any) => {
    setLoading(true);
    setErrorMessage("");

    try {
      const response = await fetch("http://cppra00a0500:9121/admin/role/create", {
        method: "POST",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json",
          "Authorization": `Bearer ${accessToken}`
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error("Failed to create role");
      }

      reset(); // Reset form after successful submission
      onClose(); // Close modal
    } catch (error: any) {
      setErrorMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Add New Role</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="block text-sm font-medium">Role Name <span className="text-red-500">*</span></label>
            <Input {...register("name", { required: "Role Name is required" })} />
            {errors.name && <p className="text-red-500 text-xs">{errors.name.message}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium">Entitlement</label>
            <Input {...register("entitlement")} />
          </div>

          <div>
            <label className="block text-sm font-medium">Description</label>
            <Input {...register("description")} />
          </div>

          {errorMessage && <p className="text-red-500 text-sm">{errorMessage}</p>}

          <DialogFooter>
            <Button type="submit" disabled={loading}>{loading ? "Adding..." : "Add Role"}</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
};

export default AddRoleModal;