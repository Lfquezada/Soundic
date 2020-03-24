ALTER TABLE customer ADD COLUMN inactive_permission BOOLEAN;
ALTER TABLE customer ADD COLUMN modify_permission BOOLEAN;
ALTER TABLE customer ADD COLUMN delete_permission BOOLEAN;
UPDATE customer SET inactive_permission=FALSE;
UPDATE customer SET modify_permission=FALSE;
UPDATE customer SET delete_permission=FALSE;