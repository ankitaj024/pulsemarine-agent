"""
Unified schema definitions for Domain Agents.
Provides agents with cross-table awareness to enable complex relational nested queries.
"""

unified_schema = """
// -------------------------------------------------
// GLOBAL ENUMS
// -------------------------------------------------

enum UserStatus { ACTIVE; INACTIVE }
enum CompanyStatus { ACTIVE; INACTIVE }
enum VesselStatus { ACTIVE; INACTIVE }
enum FleetStatus { ACTIVE; INACTIVE }

enum DefectStatus { OPEN; REPAIR_COMPLETED; CLOSED; DEFERRED; CANCELLED }
enum WorkflowStatus { IN_PROGRESS; UNDER_SUPDT_REVIEW; SUPDT_REVIEWED; UNDER_FM_REVIEW; FM_APPROVED }
enum DefectSeverity { LOW; MEDIUM; HIGH; CRITICAL }
enum EquipmentCategory { ACCOMMODATION_AND_GALLEY; AH_TOW_WINCH; AIR_CONDITIONING; AUX_ENGINES; BOW_THRUSTER; DECK_CRANES; DP_SYSTEM; ELECTRICAL_CONTROLS; GYROS; MAIN_ENGINES; MAIN_PROPULSION; BRIDGE_EQUIPMENT; DECK_EQUIPMENT; ENGINE_ROOM_EQUIPMENT; STEERING_GEAR; STERN_THRUSTER; ALTERNATORS; SAFETY; OTHERS }
enum Rank { MASTER; CHIEF_OFFICER; SECOND_OFFICER; THIRD_OFFICER; BOSUN; AB; CHIEF_ENGINEER; SECOND_ENGINEER; THIRD_ENGINEER; FOURTH_ENGINEER; ETO; FITTER; COOK; OTHERS }
enum Department { TECHNICAL; MARINE; CATERING; CREWING; HSSEQ; DIVING; CONSTRUCTION; OTHERS }
enum DefectCategory { TECHNICAL_ISSUE; LACK_OF_SPARES; PMS_COMPLIANCE; ELECTRICAL_ISSUES; BRIDGE_NAVIGATION_ISSUES; BRIDGE_COMMUNICATION_ISSUES; DP_RELATED; ADVERSE_WEATHER; UNDERWATER_ISSUES; CLIENT_RELATED; HUMAN_ERROR; MATERIAL_FAILURE; EXTERNAL; AGING; OTHERS }
enum ShoreAssistRequired { NO_ASSISTANCE; YES_TECHNICAL_SUPPORT; STANDBY_TECHNICAL_SUPPORT }
enum SparesAvailability { AVAILABLE; PARTIALLY_AVAILABLE; NOT_AVAILABLE }
enum ImpactOnOperation { NO_IMPACT; LIKELY_OFFHIRED; VESSEL_OFFHIRED }
enum PlannedMaintenanceStatus { YES; NO }
enum vesselCatagory { HARBOUR; OSV; JACKUP_BARGE }
enum vesselSubCatagory { NON_DP; DP_1; DP_2; DP_3; NON_SELF_PROPELLED; SLEF_PROPELLED; OTHER }
enum CommentType { INTERNAL; EXTERNAL }

// -------------------------------------------------
// MODELS
// -------------------------------------------------

model admin {
  id        String     @id @default(uuid())
  name      String
  email     String     @unique
  role      String     @default("SUPER-ADMIN")
  status    UserStatus @default(ACTIVE)
}

model company {
  id          String        @id @default(uuid())
  name        String
  email       String        @unique
  status      CompanyStatus @default(ACTIVE)
  isDeleted   Boolean?      @default(false)

  users      user[]
  vessels    vessel[]
  defects    defect[]
  charterers charterer[]
  tags       tag[]
  fleets     fleet[]
}

model charterer {
  id        String   @id @default(uuid())
  companyId String
  name      String
  company   company  @relation(fields: [companyId], references: [id])
}

model tag {
  id        String   @id @default(uuid())
  title     String
  companyId String
  company   company  @relation(fields: [companyId], references: [id])
}

model fleet {
  id        String      @id @default(uuid())
  name      String
  companyId String
  status    FleetStatus @default(ACTIVE)
  company   company     @relation(fields: [companyId], references: [id])
  vessels   vessel[]
  defects   defect[]
}

model role {
  id        String   @id @default(uuid())
  name      String   @unique
  users     user[]
}

model user {
  id          String     @id @default(uuid())
  name        String
  email       String     @unique
  roleId      String
  companyId   String
  status      UserStatus @default(ACTIVE)
  isDeleted   Boolean?   @default(false)
  role        role       @relation(fields: [roleId], references: [id])
  company     company    @relation(fields: [companyId], references: [id])
  createdDefects  defect[] @relation("CreatedByUser")
  assignedDefects defect[] @relation("AssignedToUser")
  vessels       vessel[]
}

model vessel {
  id                          String             @id @default(uuid())
  companyId                   String
  vesselName                  String
  imoNumber                   BigInt
  vesselCatagory              vesselCatagory?
  vesselSubCatagory           vesselSubCatagory?
  fleetId                     String?
  assignedToId                String?
  assignedTo                  user?              @relation(fields: [assignedToId], references: [id])
  status                      VesselStatus       @default(ACTIVE)
  isDeleted                   Boolean?           @default(false)

  company company  @relation(fields: [companyId], references: [id])
  fleet   fleet?   @relation(fields: [fleetId], references: [id])
  defects defect[]
}

model defect {
  id        String @id @default(uuid())
  companyId String
  vesselId  String
  defectNumber String @unique
  title String
  equipmentCategory EquipmentCategory
  severity DefectSeverity @default(MEDIUM)
  reportedByName String?
  rank Rank?
  reportedAt DateTime
  fleetId String?
  status DefectStatus @default(OPEN)
  workflowStatus WorkflowStatus @default(IN_PROGRESS)
  defectCategory DefectCategory?
  createdById String?
  assignedToId String?
  isDeleted Boolean? @default(false)

  company    company @relation(fields: [companyId], references: [id])
  vessel     vessel  @relation(fields: [vesselId], references: [id])
  fleet      fleet?  @relation(fields: [fleetId], references: [id])
  createdBy  user?   @relation("CreatedByUser", fields: [createdById], references: [id])
  assignedTo user?   @relation("AssignedToUser", fields: [assignedToId], references: [id])
  comments    defectComment[]
}

model defectComment {
  id            String      @id @default(uuid())
  defectId      String
  authorId      String
  comment       String
  commentType   CommentType @default(INTERNAL)
  defect        defect      @relation(fields: [defectId], references: [id], onDelete: Cascade)
  author        user        @relation(fields: [authorId], references: [id])
}
"""
